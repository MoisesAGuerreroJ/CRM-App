from flask import Flask, render_template, send_from_directory, jsonify
from pathlib import Path
import json
import os

app = Flask(__name__)
CONFIG_DIR = Path(os.environ.get("APP_CONFIG_DIR", "/root/config"))


def load_local_config():
    config_path = CONFIG_DIR / "local.json"
    if not config_path.is_file():
        return {}
    with config_path.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/welcome')
@app.route('/welcome.html')
def welcome():
    return render_template('welcome.html')


@app.route('/form')
@app.route('/form.html')
def form():
    return render_template('form.html')


@app.route('/formlist')
@app.route('/formlist.html')
def form_list():
    return render_template('formlist.html')


@app.route('/app-config')
def app_config():
    # Only explicitly approved presentation settings are exposed to the browser.
    config = load_local_config()
    return jsonify({
        "app_title": config.get("app_title", "CRM Application"),
        "form_title": config.get("form_title", "Customer Registration"),
        "gift_options": config.get("gift_options", []),
        "distribution_options": config.get("distribution_options", []),
        "referred_brand_question": config.get("referred_brand_question", "Additional question")
    })


@app.route('/styles/<path:filename>')
def styles_files(filename):
    return send_from_directory('/root/templates/styles', filename)


@app.route('/scripts/<path:filename>')
def scripts_files(filename):
    return send_from_directory('/root/templates/scripts', filename)


if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=int(os.environ.get('WEB_PORT', '80')), debug=debug)
