import os
import subprocess

from flask import Flask, request, render_template, abort, send_from_directory

app = Flask(__name__)


@app.route('/springViewer')
@app.route('/springViewer_1_6_dev')
@app.route('/springViewer_1_6_dev.html')
def handle_get():
    return render_template("springViewer.html")
    param = request.query_string.decode()
    return f'GET request processed with param: {param}'


@app.route('/post-endpoint', methods=['POST'])
def handle_post():
    data = request.data  # Or use request.form for form-encoded data
    # Process your POST data here
    return 'POST request processed'


ALLOWED_EXTENSIONS = {'txt', 'json', 'csv', 'js', 'css', 'html'}

base_directory = os.path.dirname(os.path.abspath(__file__))
scripts_folder = "cgi-bin"


@app.route(f'/{scripts_folder}/<script_name>', methods=['POST'])
def run_script(script_name):
    # Security check: Ensure the script name does not contain any directory parts
    if '/' in script_name or '\\' in script_name:
        abort(404)

    # Check that it's a Python script
    if not script_name.endswith('.py'):
        abort(404)

    # Construct the full path to the script
    script_path = os.path.join(base_directory, scripts_folder, script_name)

    # Check if the script exists
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


@app.route('/<path:filepath>', methods=['GET'])
def serve_file(filepath):
    # Check if the path is safe
    if '..' in filepath or filepath.startswith('/'):
        abort(404)  # Not found for security reasons

    # Extract the file extension and check if it's allowed
    file_extension = os.path.splitext(filepath)[1].lstrip('.').lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        abort(404)  # Not found if the file extension is not allowed

    # Full path to the file
    full_path = os.path.join(base_directory, filepath)

    # Check if the file exists
    if not os.path.isfile(full_path):
        abort(404)  # Not found

    # Serve the file content
    return send_from_directory(base_directory, filepath)


if __name__ == '__main__':
    app.run(port=8000)
