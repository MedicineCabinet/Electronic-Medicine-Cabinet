from flask import Flask, render_template, redirect, url_for, request, session, flash, make_response
import datetime

app = Flask(__name__)
app.secret_key = '8d63cfa786bdee8fb79dbad79110d5c1'

# Dummy user data for demonstration
users = {"username123": "password123"}

#Session Timeout functinality
@app.before_request
def session_management():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=1)  # Set the session timeout (e.g., 1 minute)
    session.modified = True

    if 'user' in session:
        session['last_activity'] = datetime.datetime.now()

#Routing for the Login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'] 
        password = request.form['password']
        remember_me = 'remember_me' in request.form

        if username in users and users[username] == password:
            session['user'] = username  # Store the username in the session

            resp = make_response(redirect(url_for('home')))
            
            if remember_me:
                # Set cookies to remember the username and password for 30 days
                resp.set_cookie('username', username, max_age=30*24*60*60)
                resp.set_cookie('password', password, max_age=30*24*60*60)
                resp.set_cookie('remember_me', 'checked', max_age=30*24*60*60)
            else:
                # Clear the cookies if "Remember Me" is not checked
                resp.delete_cookie('username')
                resp.delete_cookie('password')
                resp.delete_cookie('remember_me')
                
            return resp
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

#Routing for the Home page
@app.route('/home')
def home():
    if 'user' in session:
        last_activity = session.get('last_activity')
        now = datetime.datetime.now()
        if last_activity and (now - last_activity).total_seconds() > 3600:  # 1 hour of inactivity
            flash('You have been automatically logged out due to inactivity', 'warning')
            return redirect(url_for('logout'))
        return render_template('home.html', user=session['user'], content='inventory.html')
    else:
        return redirect(url_for('login'))

#Adding the functionality of Logout and Automatic Logout during Idle
@app.route('/logout')
def logout():
    session.pop('user', None)
    idle = request.args.get('idle')
    resp = make_response(redirect(url_for('login', idle=idle)))
    # Clear cookies on logout
    resp.delete_cookie('username')
    resp.delete_cookie('password')
    resp.delete_cookie('remember_me')
    return resp

@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

@app.route('/doorlogs')
def doorlogs():
    return render_template('doorlogs.html')


@app.route('/notification')
def notification():
    return render_template('notification.html')

@app.route('/accounts')
def accounts():
    return render_template('accounts.html')


if __name__ == '__main__':
    app.run(debug=True)
