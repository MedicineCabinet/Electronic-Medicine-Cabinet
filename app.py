from flask import Flask, render_template, redirect, url_for, request, session, flash, make_response

app = Flask(__name__)

# Set a secret key for session management
app.secret_key = '8d63cfa786bdee8fb79dbad79110d5c1'

# Dummy user data for demonstration
users = {"username123": "password123"}

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

@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html', user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    resp = make_response(redirect(url_for('login')))
    # Clear cookies on logout
    resp.delete_cookie('username')
    resp.delete_cookie('password')
    resp.delete_cookie('remember_me')
    return resp

if __name__ == '__main__':
    app.run(debug=True)
