from flask import Flask
app = Flask (__name__)

@app.route("/")
def index ():
    return 'hello world to my SSIS using flask!'

app.run(debug=True)