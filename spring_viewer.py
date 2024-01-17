import errno
import socket
import threading
import webbrowser

from flask_server import run_server, DEFAULT_PORT


VIEWER_FILE = "springViewer_1_6_dev.html"


def _run_server_in_thread(debug: bool, port: int):
    def start_server():
        run_server(debug=debug, port=port)

    # Start the Flask server in a new thread
    server_thread = threading.Thread(target=start_server)
    server_thread.start()


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


def open(path="data/organoids/adata_36h_perturb_processed_09282020/all_cells", debug: bool = False):
  port = find_available_port()
  _run_server_in_thread(debug=debug, port=port)
  url = f"http://localhost:{port}/{VIEWER_FILE}?{path}"
  webbrowser.open_new_tab(url)


if __name__ == '__main__':
    open()
