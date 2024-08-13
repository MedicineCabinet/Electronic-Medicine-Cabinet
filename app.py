from flask import Flask, render_template, redirect, url_for, request, session, flash

app = Flask(__name__)

# Set a secret key for session management
app.secret_key = '8d63cfa786bdee8fb79dbad79110d5c1'

# Dummy user data for demonstration
users = {"user@example.com": "password123"}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email] == password:
            session['user'] = email
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')
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
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
