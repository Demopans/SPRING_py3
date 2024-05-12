import argparse
import os
import subprocess

from flask import Flask, request, abort, send_from_directory

parser = argparse.ArgumentParser(description='Start Flask server with optional debugging and port specification.')

parser.add_argument('-d', '--debug', action='store_true', help='run the server in debug mode')

DEFAULT_PORT = 8000
parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT, help='set the port for the server')

HOST = "localhost"
parser.add_argument('-m', '--host', type=str, default=HOST, help='sets ip address of server')

args = parser.parse_args()

app = Flask(__name__)

this_directory = os.path.dirname(os.path.abspath(__file__))

ALLOWED_EXTENSIONS = {
    'txt',
    'json',
    'csv',
    'js',
    'css',
    'html',
    'png',
    'svg',
    'gif',
    'map',
    'ico',
}

SCRIPTS_FOLDER = "cgi-bin"


@app.route('/<path:file_path>', methods=['GET'])
def serve_file(file_path):
    # Don't allow paths which exit this directory
    if '..' in file_path:
        abort(400)

    # Extract the file extension and check if it's allowed
    file_extension = os.path.splitext(file_path)[1].lstrip('.').lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        print(f"400 Unsupported File Extension: {file_extension}")
        abort(400)

    # Check if the file exists
    full_path = os.path.join(this_directory, file_path)
    if not os.path.isfile(full_path):
        abort(404)

    # Serve the file content
    return send_from_directory(this_directory, file_path)


@app.route(f'/{SCRIPTS_FOLDER}/<script_name>.py', methods=['POST'])
def run_script(script_name):
    # Don't allow paths which exit this directory
    if '..' in script_name:
        abort(400)

    # Check if the script exists
    script_path = os.path.join(
        this_directory, SCRIPTS_FOLDER, script_name) + ".py"
    if not os.path.isfile(script_path):
        abort(404)

    # Convert form data to a string
    form_data_str = '&'.join(
        f"{key}={value}" for key, value in request.form.items())

    # Execute the script
    try:
        result = subprocess.run(
            ['python', script_path], input=form_data_str, text=True, capture_output=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        abort(500, description=e.stderr)


def run_server(port: int = DEFAULT_PORT, debug: bool = False, host: str = "localhost"):
    app.run(port=port, debug=debug, host=host)


if __name__ == '__main__':
    run_server(port=args.port, debug=args.debug, host=args.host)
