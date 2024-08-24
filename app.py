from flask import Flask, render_template, redirect, url_for, request, session, flash, make_response
import datetime

app = Flask(__name__)
app.secret_key = '8d63cfa786bdee8fb79dbad79110d5c1'

# Dummy user data for demonstration
users = {"username123": "password123"}

@app.before_request
def session_management():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=5)  # Set the session timeout (e.g., 5 minutes)
    session.modified = True

    if 'user' in session:
        session['last_activity'] = datetime.datetime.now()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'] 
        password = request.form['password']
        remember_me = 'remember_me' in request.form

        if username in users and users[username] == password:
            session['user'] = username
            session['last_activity'] = datetime.datetime.now()  # Set last activity time

            resp = make_response(redirect(url_for('home')))
            
            if remember_me:
                resp.set_cookie('username', username, max_age=30*24*60*60)
                resp.set_cookie('password', password, max_age=30*24*60*60)
                resp.set_cookie('remember_me', 'checked', max_age=30*24*60*60)
            else:
                resp.delete_cookie('username')
                resp.delete_cookie('password')
                resp.delete_cookie('remember_me')
                
            return resp
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/home')
def home():
    if 'user' in session:
        last_activity = session.get('last_activity')
        now = datetime.datetime.now()
        if last_activity and (now - last_activity).total_seconds() > 300:  # 5 minutes of inactivity
            return redirect(url_for('logout'))
        return render_template('home.html', user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('username')
    resp.delete_cookie('password')
    resp.delete_cookie('remember_me')
    return resp

if __name__ == '__main__':
    app.run(debug=True)
