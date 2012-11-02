from flask import Flask, flash, render_template, request, redirect, url_for, session
from datetime import datetime
from data import Request, FollowUp
import os

app = Flask(__name__)
app.secret_key = "asdfalsdkfg38asdfl38as8dfa8"
pword = os.getenv('SANDYLOGIN', 'test')

def isMod():
    return session.get('loggedin', False)

def render(*args, **kwargs):
    print 'RENDERING...'
    kwargs['ismod'] = isMod()
    return render_template(*args, **kwargs)

#-- Static Routes --
@app.route('/login/<pw>')
def routeLogin(pw=None):
    if pw == pword:
        session['loggedin'] = True
        return redirect('/responses')
    flash('Bad password!', 'error')
    return redirect('/')

@app.route('/logout')
def routeLogout():
    session['loggedin'] = False
    return redirect('/')

@app.route('/')
def routeIndex(): return render('index.html')

@app.route('/post')
def routePost(): return render('post.html')

@app.route('/find') #@TODO Pagination (sort invalid)
@app.route('/find/<page>')
def routeSearch(page=1):
    try: reqs = Request.objects().paginate(page=int(page), per_page=35) #@NOTE Hacky af
    except: return redirect('/find/%s' % (int(page)-1))
    return render('find.html', reqs=reqs, page=int(page))

@app.route('/responses')
@app.route('/responses/<page>')
def routeResponese(page=1):
    try: reqs = FollowUp.objects().paginate(page=int(page), per_page=35)
    except: return redirect('/responses/%s' % (int(page)-1))
    return render('mod.html', reqs=reqs, page=int(page))

# -- Dynamic Stuffs --
@app.route('/mod/<action>/<id>')
def routeMod(id=None, action=None):
    if not isMod(): return redirect(url_for('/find'))
    if not id: return render('find.html', reqs=Request.objects())
    if action == 'valid_resp':
        q = FollowUp.objects(id=id)
        if not len(q): 
            flash("Invalid response ID!", 'error')
            return redirect('/responses')
        q = q[0]
        q.valid = True
        q.save()
        flash('Marked response as valid!', 'success')
        return redirect('/responses')

    elif action == 'delete_resp':
        q = FollowUp.objects(id=id)
        if not len(q): 
            flash("Invalid response ID!", 'error')
            return redirect('/responses')
        q[0].delete()
        flash('Deleted response!', 'success')
        return redirect('/responses')
    elif action == 'delete_req':
        q = Request.objects(id=id)
        if not len(q):
            flash("Invalid response ID!", 'error')
            return redirect('/find')
        q[0].delete()
        flash("Marked request %s as invalid!" % id, 'success')
        return redirect('/find')

@app.route('/help/<id>')
def routeHelp(id):
    if not id:
        return redirect(url_for('/find'))
    p = Request.objects(id=id)
    if not len(p):
        return "No such request ID '%s'" % id
    return render('help.html', p=p[0])

@app.route('/resp/<id>')
def routeResp(id):
    if not id:
        return redirect(url_for('/post'))
    p = FollowUp.objects(id=id)
    if not len(p):
        return "No such response ID '%s'" % id
    if p[0].valid:
        flash("""Your help is needed! Please click <a href='/resp/%s/info'>here</a> to get contact information! 
        Make sure to follow up on this page to help us keep efforts organized and managed!""" % (p[0].id), 'success')
        return render('base.html')
    else:
        flash("Your post is still waiting moderation!", 'error')
        return render('base.html', autoref=True)

@app.route('/resp/<id>/info')
def routeRespInfo(id):
    if not id:
        return redirect(url_for('/post'))
    p = FollowUp.objects(id=id)
    if not len(p): 
        return "No such response ID '%s'" % id
    if not p[0].valid:
        return redirect(url_for('/resp/%s' % id))
    p = p[0]
    p.connected = True
    p.entry.connected = True
    p.entry.save()
    p.save()
    flash("Please contact the person with this information: %s" % p.entry.contact, 'success') #@TODO More info here?
    return render('base.html')

@app.route('/internals/<route>', methods=['POST'])
def internals(route=None):
    if route == 'needhelp':
        for k, v in request.form.items():
            if not v: 
                flash('No fields can be empty!', 'error')
                return redirect('/post')
        obj = Request(
            name=request.form.get('name'),
            urgent={'on':True, 'off':False, None:False}[request.form.get('urgent')],
            request=request.form.get('request'),
            contact=request.form.get('phonenum'),
            location=request.form.get('location'))
        obj.save()
        flash("Your request has been submitted to the system! We'll try to get to it ASAP.<br />Request ID: %s" % obj.id, 'success')
        return redirect('/post')

    elif route == "canhelp":
        for k, v in request.form.items():
            if not v: 
                flash('You must give a value for %s! <a href="/help/%s">Try again</a>' % (k, request.form.get('id')), 'error')
                return redirect('/find')

        p = Request.objects(id=request.form.get('id'))
        if not len(p): 
            flash('Could not find the request ID "%s"' % id, 'error')
            return redirect('/find')

        p = p[0]
        obj = FollowUp(
            name=request.form.get('name'),
            cangive=request.form.get('have'),
            contact=request.form.get('phonenum'),
            entry=p)
        obj.save()
        p.responses.append(obj)
        flash("""
            Your response has been filed, please check back at <a href="/resp/%s">your response page</a> often. 
            We'll update the page as soon as you can help!""" % (obj.id), 'success')
        return redirect('/find')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv('PORT', 5000)))
