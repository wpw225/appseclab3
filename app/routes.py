from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from app.models import User
from app import db
from app.forms import RegistrationForm
from app.forms import PostForm
from app.models import Post
#from urlparse import urlparse
from urllib.parse import urlparse
from subprocess import check_output
from talisman import Talisman,ALLOW_FROM

SELF = "'self'"
print(SELF)
talisman = Talisman(
    app,
    content_security_policy={
        'default-src': SELF,
        'img-src': '*',
        'script-src': SELF,
        'style-src': [
            SELF
        ],
    },
    force_https=True,
    force_https_permanent=False,
    strict_transport_security=False
)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/spell_check', methods=['GET', 'POST'])
@login_required
@talisman(
    frame_options='ALLOW-FROM',
    frame_options_allow_from='https://127.0.0.1:5000/',
)

def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Added spellcheck search to database')
        #return redirect(url_for('index'))
        with open('test.txt',"w") as fo:
            fo.write(post.body)
        output = check_output(["./a.out","test.txt","wordlist.txt"])
        return render_template('index.html', title='Home', post=post, result=output.decode('UTF-8'))
    #post = current_user.spellcheck_lastpost()
    return render_template('index.html', title='Home', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    #output = "anything" 
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        #output = "User already logged in"
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.uname.data).first()
        if user is None or not user.check_password(form.pword.data):
            #output = "Incorrect username or password"
            #return render_template('login.html', title='Sign In', form=form, output=output)
            flash('Incorrect username or password')
            return redirect(url_for('login'))
        if not user.check_password2(form.pword2.data):
            #output = "Two-factor authentication failure"
            #return render_template('login.html', title='Sign In', form=form, output=output)
            flash('Two-factor authentication failure')
            return redirect(url_for('login'))
        flash('Success - User Login Request')
        #output = "Success - User Login Request"
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page) #avoid redirect
        #return render_template('login.html', title='Sign In', form=form, output=output)
    return render_template('login.html', title='Sign In', form=form) #add output=output

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
#        user = User(username=form.uname.data, email=form.email.data)
        user = User(username=form.uname.data)
        user.set_password(form.pword.data)
        user.set_password2(form.pword2.data)
        db.session.add(user)
        db.session.commit()
        flash('Success - User Registration Request')
        return redirect(url_for('login'))
#    else:
#        flash('Failure - User Registration Request')
#        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

