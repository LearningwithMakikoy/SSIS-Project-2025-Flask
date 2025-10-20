from flask import Flask, render_template
from app import create_app

app = create_app()

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

@app.route('/')
def index():
    return render_template('layouts/index.html')

@app.route('/students')
def students():
    return render_template('layouts/students.html')

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('layouts/login.html')

@app.route('/admin/create')
def admin_create():
    return render_template('layouts/admin_create.html')

if __name__ == '__main__':
    app.run(debug=True)
