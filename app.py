from flask import Flask, render_template, request, redirect
from datetime import datetime
from data import Request
app = Flask(__name__)

@app.route('/')
def routeIndex():
    return render_template('index.html')

@app.route('/find')
def routeSearch():
    return render_template('find.html', reqs=Request.objects())

@app.route('/post')
def routePost():
    return render_template('post.html')

@app.route('/internals/<route>', methods=['POST'])
def internals(route=None):
    print request.form
    if route == 'needhelp':
        for k, v in request.form.items():
            if not v: 
                return 'You must give a value for %s! <a href="/post">Try again</a>' % k 
        obj = Request(
            name=request.form.get('name'),
            urgent={'on':True, 'off':False, None:False}[request.form.get('urgent')],
            request=request.form.get('request'),
            contact=request.form.get('phonenum'),
            location=request.form.get('location'))
        obj.save()
        return "Your request has been submitted to the system! We'll try to get to it ASAP. Request ID: %s" % obj.id 


if __name__ == "__main__":
    app.run(debug=True)