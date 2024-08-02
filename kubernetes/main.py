import argparse
import json
import pprint

from kubernetes import client, config

CONFIG_MAPS_TO_IGNORE = {"kube-root-ca.crt"}

def main():
    parser = argparse.ArgumentParser(description="BLAHBLAH")
    parser.add_argument("namespace", type=str, help="The namespace to clean up")
    parser.add_argument("--wet-run", type=bool, default=False, help="When set to true, perform deletes.")

    args = parser.parse_args()

    _main(args.namespace, args.wet_run)

def _main(namespace: str, wet_run: bool) -> None:
    try:
        # Try to load config from the kube-config file. This is useful if
        # running on a machine that has access to a cluster.
        config.load_kube_config()
    except:
        # Use the Service account given to a Pod.
        config.load_incluster_config()

    apps_v1 = client.AppsV1Api()
    batch_v1 = client.BatchV1Api()
    # No, these key names are not pep-8 compliant but they are used
    # in output intended for humans and I don't want to write
    # formatting code.
    cms_in_use = {
        "Deployment": _get_referenced_config_maps(apps_v1.list_namespaced_deployment(namespace)),
        "ReplicaSet": _get_referenced_config_maps(apps_v1.list_namespaced_replica_set(namespace)),
        "StatefulSet": _get_referenced_config_maps(apps_v1.list_namespaced_stateful_set(namespace)),
        "Job": _get_referenced_config_maps(batch_v1.list_namespaced_job(namespace)),
        "CronJob": _get_referenced_config_maps(batch_v1.list_namespaced_cron_job(namespace)),
    }
    _generate_cms_in_use_report(cms_in_use)

    present_cms = _get_all_config_map_names(namespace)
    flattened_refd = _flatten_cms_in_use(cms_in_use)

    cms_not_referenced = present_cms - flattened_refd
    _generate_cms_not_in_use_report(cms_not_referenced)

def _get_referenced_config_maps(resource_list) -> dict:
    referenced_cms = {}
    for resource in resource_list.items:
        num_refd, refs = _get_cms_from_pod_spec(resource.spec.template.spec)
        if num_refd > 0:
            referenced_cms[resource.metadata.name] = refs
    return referenced_cms

def _get_cms_from_pod_spec(spec: client.models.v1_pod_spec.V1PodSpec) -> (int, dict):
        num_refd = 0
        cms_in_use = {
            "volumes": [],
            "env": [],
            "init_container_env": []
        }
        if spec.volumes is not None:
            for v in spec.volumes:
                if v.config_map is not None:
                    if v.config_map.name not in cms_in_use["volumes"]:
                        cms_in_use["volumes"].append(v.config_map.name)
                        num_refd += 1

        if spec.volumes is not None:
            for c in spec.containers:
                for e in c.env:
                    if e.value_from is not None:
                        if e.value_from.config_map_key_ref is not None:
                            if e.value_from.config_map_key_ref.name not in cms_in_use["env"]:
                                cms_in_use["env"].append(e.value_from.config_map_key_ref.name)
                                num_refd += 1

        if spec.init_containers is not None:
            for c in spec.init_containers:
                for e in c.env:
                    if e.value_from is not None:
                        if e.value_from.config_map_key_ref is not None:
                            if e.value_from.config_map_key_ref.name not in cms_in_use["init_container_env"]:
                                cms_in_use["init_container_env"].append(e.value_from.config_map_key_ref.name)
                                num_refd += 1

        return num_refd, cms_in_use


def _get_all_config_map_names(namespace) -> set[str]:
    core_v1 = client.CoreV1Api()
    cms = core_v1.list_namespaced_config_map(namespace)
    return set([cm.metadata.name for cm in cms.items if cm.metadata.name not in CONFIG_MAPS_TO_IGNORE])

def _flatten_cms_in_use(cms_in_use) -> set[str]:
    _cms_in_use = []
    for v in cms_in_use.values():
        for k,x in v.items():
            for source, cm_name in x.items():
                _cms_in_use.extend(cm_name)
    return set(_cms_in_use)

def _generate_cms_in_use_report(cms_in_use) -> None:
    title = "Configmaps currently referenced by Deployments, ReplicaSets, StatefulSets, Jobs and CronJobs"
    print(title)
    print("="*len(title))
    print()
    row_fmt = "{:<20} {:<60} {:<20} {:<60}"
    print(row_fmt.format('Resource Type', 'Resource Name', 'Reference Type', 'ConfigMap Name'))
    for r_type, x in cms_in_use.items():
        for r_name,v in x.items():
            for ref_type, names in v.items():
                for name in names:
                    print(row_fmt.format(r_type, r_name, ref_type, name))
    print()

def _generate_cms_not_in_use_report(cms_not_referenced: set[str]) -> None:
    print("{} ConfigMaps were identified for cleanup.".format(len(cms_not_referenced)))
    for cm_name in sorted(cms_not_referenced):
        print(cm_name)
    print()


if __name__ == "__main__":
    main()
