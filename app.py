from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from data import Request, FollowUp
app = Flask(__name__)

#-- Static Routes --
@app.route('/')
def routeIndex(): return render_template('index.html')

@app.route('/find') #@TODO Pagination
def routeSearch(): return render_template('find.html', reqs=Request.objects())

@app.route('/post')
def routePost(): return render_template('post.html')

# -- Dynamic Stuffs --
#We dont pretend this is secure, but it will have todo for now
@app.route('/mod/<pw>')
@app.route('/mod/<pw>/<rid>')
def routeMod(rid=None, pw=None):
    if not rid:
        return render_template('mod.html', reqs=Request.objects())

@app.route('/help/<id>')
def routeHelp(id):
    if not id:
        return redirect(url_for('/find'))
    p = Request.objects(id=id)
    if not len(p):
        return "No such request ID '%s'" % id
    return render_template('help.html', p=p[0])

@app.route('/resp/<id>')
def routeResp(id):
    if not id:
        return redirect(url_for('/post'))
    p = FollowUp.objects(id=id)
    if not len(p):
        return "No such response ID '%s'" % id
    if p[0].valid:
        return """Your help is needed! Please click <a href='/resp/%s/info'>here</a> to get contact information! 
        Make sure to follow up on this page to help us keep efforts organized and managed!""" % (p.id)
    else:
        return "Your post is still waiting moderation!" #@TODO Refresh page every x mins?

@app.route('/resp/<id>/info')
def routeRespInfo(id):
    if not id:
        return redirect(url_for('/post'))
    p = FollowUp.objects(id=id)
    if not len(p): return "No such response ID '%s'" % id
    if not p[0].valid:
        return redirect(url_for('/resp/%s' % id))
    p[0].connected = True
    p[0].save()
    return "Please contact the person with this information: %s" % p[0].entry.contact


@app.route('/internals/<route>', methods=['POST'])
def internals(route=None):
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
    elif route == "canhelp":
        for k, v in request.form.items():
            if not v: 
                return 'You must give a value for %s! <a href="/help/%s">Try again</a>' % (k, request.form.get('id'))
        p = Request.objects(id=request.form.get('id'))
        if not len(p): return 'Could not the request ID "%s"' % id
        p = p[0]
        obj = FollowUp(
            name=request.form.get('name'),
            cangive=request.form.get('have'),
            contact=request.form.get('phonenum'),
            entry=p)
        obj.save()
        p.responses.append(obj)
        return """
        Your response has been filed, please check back at <a href="/resp/%s">your response page</a> often. 
        We'll update the page as soon as you can help!""" % (obj.id)

if __name__ == "__main__":
    app.run(debug=True)