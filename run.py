from flask import Flask, render_template

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students')
def students():
    return render_template('students.html')

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/admin/create')
def admin_create():
    return render_template('admin_create.html')

if __name__ == '__main__':
    app.run(debug=True)
