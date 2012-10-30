from flask import Flask, render_template, request, redirect
from data import Market

#@TODO Captcha

app = Flask(__name__)

@app.route('/')
def routeIndex():
    return render_template('index.html')

@app.route('/find')
def routeSearch():
    return render_tempalte('find.html')

@app.route('/post')
def routePost():
    return render_template('post.html')

@app.route('/internals/<route>', methods=['POST'])
def internals(route=None):
    if route == 'needhelp': pass
    return "Your request has been sent and will be processed ASAP!" #@TODO give a request ID for tracking


if __name__ == "__main__":
    app.run(debug=True)