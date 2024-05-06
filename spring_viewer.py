import errno
import os
import socket
import threading
import webbrowser

from flask_server import run_server, DEFAULT_PORT


VIEWER_FILE = "springViewer_1_6_dev.html"

this_directory = os.path.dirname(os.path.abspath(__file__))


def _path_is_valid(path: str) -> bool:
    # TODO: do more checks to see if this is a valid SPRING directory
    path_from_here = os.path.join(this_directory, path)
    return os.path.isdir(path) or os.path.isdir(path_from_here)


def find_available_port(start_port=DEFAULT_PORT, num_ports_to_try=50):
    end_port = start_port + max(num_ports_to_try, 1)
    for port in range(start_port, end_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError as e:
                if e.errno == errno.EADDRINUSE:
                    continue
                raise e
    raise RuntimeError(
        f"No available ports found between {start_port} and {end_port-1}."
    )


def _run_server_in_thread(port: int):
    def start_server():
        run_server(port=port)

    # Start the Flask server in a new thread
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    return server_thread


def open_plot_from_directory(path: str):
    if not _path_is_valid(path):
        raise RuntimeError(f"Path not valid: {path}")

    port = find_available_port()
    server_thread = _run_server_in_thread(port=port)

    url = f"http://localhost:{port}/{VIEWER_FILE}?{path}"
    webbrowser.open_new_tab(url)

    server_thread.join()


if __name__ == '__main__':
    open_plot_from_directory(
        "datasets/XA23_s10/PGCs"
    )
