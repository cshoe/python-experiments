from pip.index import PackageFinder
from pip.locations import build_prefix, src_prefix
from pip.req import InstallRequirement, RequirementSet


def main():
    requirement_set = RequirementSet(
        build_dir=build_prefix,
        src_dir=src_prefix,
        download_dir=None)

    requirement_set.add_requirement(InstallRequirement.from_line('git+ssh://git@github.com/arc90/readability-selectors@5-bootstrap#egg=rdbselectors', None))

    install_options = []
    global_options = []
    finder = PackageFinder(find_links=[], index_urls=['http://pypi.python.org/simple/'])

    requirement_set.prepare_files(finder, force_root_egg_info=False, bundle=False)
    requirement_set.install(install_options, global_options)

    print '\n'
    print 'Installed'
    print '=================================='
    names = [package.name for package in requirement_set.successfully_installed]
    print names
    print '\n'

    pass


if __name__ == '__main__':
    main()
