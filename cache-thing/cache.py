import logging
import multiprocessing
import re
import socket

from typing import Dict, List, Tuple


logging.basicConfig(level=logging.DEBUG)
KEYS_VALIDATOR = re.compile(r'[A-Za-z0-9_-]*')


def handle_client(cache_data: Dict[bytes, Tuple[bytes, int]], conn: socket.socket, address: Tuple[str, int]):
    """
    Handle a new client connecting to a CacheServer instance.
    """
    logger = logging.getLogger("Client Process - {}".format(address))
    try:
        buffer = []
        while True:
            data = conn.recv(1024)
            if data == b"":
                logger.debug("Connection closed remotely")
                break
            # Prevent the ending newline from going into the buffer
            buffer.append(data[:-1])
            logger.debug("Data recieved %s", data)
            # at this point, the buffer should contain the command
            if data[-1:] == b"\n":
                logger.debug("Handling command")
                # end of a command
                response = _handle_command(cache_data, conn, b"".join(buffer))
                conn.send(response)
                # reset buffer before reading more from the connection
                buffer = []
    except:
        logger.exception("Problem handling request")
    finally:
        logger.info("Closing connection")
        conn.close()


def _handle_command(cache_data: Dict[bytes, Tuple[bytes, int]], conn: socket.socket, cmd: bytes) -> bytes:
    parts = cmd.split(b" ")
    cmd_name = parts[0]
    if cmd_name == b"get":
        return _get_command(cache_data, parts[1:])
    elif cmd_name == b"set":
        return _set_command(cache_data, conn, parts[1:])
    else:
        return b"INVALID: Unknown cmd\n"


def _get_command(cache_data: Dict[bytes, Tuple[bytes, int]], keys: list) -> bytes:
    response: List[bytes] = []
    for key in keys:
        ascii_key = key.decode("ascii")
        if KEYS_VALIDATOR.fullmatch(ascii_key) == None:
            # TODO: log this
            continue
        try:
            value, byte_cnt = cache_data[key]
        except KeyError:
            # TODO: Log this
            continue
        else:
            response.append(bytes("VALUE {} {}".format(ascii_key, byte_cnt), "ascii"))
            response.append(value)

    # Have to add the new line to the last entry since the join below doesn't.
    response.append(b"END\n")
    return b"\n".join(response)


def _set_command(cache_data: Dict[bytes, Tuple[bytes, int]], conn: socket.socket, cmd_args: list) -> bytes:
    if len(cmd_args) > 3:
        return b"INVALID: Too many args\n"
    byte_cnt = 0
    try:
        byte_cnt = int(cmd_args[1], 10)
    except ValueError:
        return b"INVALID: Invalid byte count\n"
    
    if KEYS_VALIDATOR.fullmatch(cmd_args[0].decode("ascii")) == None:
        return b"INVALID: Invalid key\n"

    # Read the value off the connection
    # byte_cnt + 2 for the \n
    value = conn.recv(byte_cnt + 2)
    if value[-1:] != b"\n":
        return b"INVALID: Value missized\n"

    cache_data[cmd_args[0]] = (value[:-1], byte_cnt)
    return b"STORED\n"


class CacheServer(object):
    def __init__(self, hostname, port, backlog=1):
        """TODO: Docstring for __init__.

        :hostname: TODO
        :port: TODO
        :returns: TODO

        """
        self.logger = logging.getLogger("CacheServer")
        self.hostname = hostname
        self.port = port
        self.backlog = backlog
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))

    def start(self):
        self.socket.listen(self.backlog)
        self.logger.debug("Listening")

        with multiprocessing.Manager() as manager:
            cache_data = manager.dict()
            while True:
                # This blocks until a connection is accepted
                conn, address = self.socket.accept()
                self.logger.debug("Got connection")
                process = multiprocessing.Process(target=handle_client,
                                                  args=(cache_data, conn, address), daemon=True)
                process.start()
                self.logger.debug("Started process %r", process)

    def stop(self):
        self.logger.debug("Stopping")
        self.logger.debug("Terminating processes")
        for process in multiprocessing.active_children():
            process.terminate()
            process.join()
            process.close()
        self.logger.debug("Closing socket")
        self.socket.close()
        self.logger.debug("Server stopped")


def main():
    logger = logging.getLogger("main")
    server = CacheServer("127.0.0.1", 11211)
    try:
        logger.debug("Starting server")
        server.start()
    except:
        logging.exception("Exception thrown when server running")
    finally:
        logging.info("Stopping server")
        server.stop()

if __name__ == "__main__":
    main()
