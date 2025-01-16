from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the main page
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

# Route for the form page
@app.route('/form')
def form():
     return render_template('form.html')

# Route for the form list page
@app.route('/formlist')
def form_list():
    return render_template('formlist.html')

# Route to serve static files from styles directory
@app.route('/styles/<path:filename>')
def styles_files(filename):
     return send_from_directory('/root/templates/styles', filename)

# Route to serve static files from scripts directory
@app.route('/scripts/<path:filename>')
def scripts_files(filename):
    return send_from_directory('/root/templates/scripts', filename)

# Catch all route
@app.route('/<path:filename>')
def root_files(filename):
    if filename.endswith(".html"):
        return send_from_directory('/root/templates',filename)
    return send_from_directory('/root', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)