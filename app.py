from flask import Flask, render_template, redirect, url_for, request, session, flash, make_response
import datetime
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="", 
    database="db_medicine_cabinet"
)

app = Flask(__name__)
app.secret_key = '8d63cfa786bdee8fb79dbad79110d5c1'

# Dummy user data for demonstration
users = {"username123": "password123"}

#Session Timeout functinality
@app.before_request
def session_management():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=10)  # Set the session timeout (e.g., 1 minute)
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
    search_term = request.args.get('search', '').lower()

    # Fetch data from the database
    cursor = conn.cursor(dictionary=True)  # Use dictionary=True to get results as dictionaries
    try:
        cursor.execute("SELECT name, type, quantity, unit, date_stored, expiration_date FROM medicine_inventory")
        # Get all inventory items from the database
        inventory_items = cursor.fetchall()

        # Filter inventory based on search term
        if search_term:
            filtered_items = [
                item for item in inventory_items if (
                    search_term in item["name"].lower() or
                    search_term in item["type"].lower() or
                    search_term in str(item["quantity"]) or
                    search_term in item["date_stored"].isoformat().lower() or
                    search_term in item["expiration_date"].isoformat().lower()
                )
            ]
        else:
            filtered_items = inventory_items

    except Exception as e:
        # Handle exceptions such as database errors
        filtered_items = []
        print(f"Database error: {e}")  # Log the error (or use a logger)
    finally:
        cursor.close()

    # Check if the request is via AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('inventory_table_rows.html', inventory_items=filtered_items)

    # Render the full page if not AJAX
    return render_template('inventory.html', inventory_items=filtered_items)


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
