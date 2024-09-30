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
            sort_by = request.args.get('sort_by', 'name')  # Default to sorting by name
            order = request.args.get('order', 'asc')  # Default to ascending order

            # Ensure that only valid column names are used for sorting
            valid_sort_columns = ['name', 'type', 'quantity', 'unit', 'date_stored', 'expiration_date']
            if sort_by not in valid_sort_columns:
                sort_by = 'name'  # Default to sorting by name if an invalid column is provided

            # Use SQL-specific handling for numeric sorting when sorting by quantity
            sort_column = 'CAST(quantity AS UNSIGNED)' if sort_by == 'quantity' else sort_by

            # Set the sort order (asc or desc)
            sort_order = 'ASC' if order == 'asc' else 'DESC'

            # Fetch data from the database
            cursor = conn.cursor(dictionary=True)
            try:
                # Modify query to include sorting
                query = f"SELECT name, type, quantity, unit, date_stored, expiration_date FROM medicine_inventory ORDER BY {sort_column} {sort_order}"
                cursor.execute(query)
                inventory_items = cursor.fetchall()

                # Filter inventory based on search term if applicable
                if search_term:
                    filtered_items = [
                        item for item in inventory_items if (
                            search_term in item["name"].lower() or
                            search_term in item["type"].lower() or
                            search_term in str(item["quantity"]) or
                            search_term in item["unit"].lower() or
                            search_term in item["date_stored"].isoformat().lower() or
                            search_term in item["expiration_date"].isoformat().lower()
                        )
                    ]
                else:
                    filtered_items = inventory_items

            except Exception as e:
                filtered_items = []
                print(f"Database error: {e}")  # Log the error
            finally:
                cursor.close()

            # If it's an AJAX request, return only the table rows
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return render_template('inventory_table_rows.html', inventory_items=filtered_items)

            # Render full page otherwise
            return render_template('inventory.html', inventory_items=filtered_items)       

@app.route('/doorlogs')
def doorlogs():
    search_term = request.args.get('search', '').lower()
    sort_by = request.args.get('sort_by', 'username')  # Default to sorting by time
    order = request.args.get('order', 'asc')  # Default to ascending order

    valid_sort_columns = ['username', 'accountType', 'position', 'date', 'time', 'action_taken']
    if sort_by not in valid_sort_columns:
        sort_by = 'username'  # Default to sorting by time

    sort_order = 'ASC' if order == 'asc' else 'DESC'

    cursor = conn.cursor(dictionary=True)
    try:
        query = f"SELECT username, accountType, position, date, time, action_taken FROM door_logs ORDER BY {sort_by} {sort_order}"
        cursor.execute(query)
        door_logs = cursor.fetchall()

        if search_term:
            filtered_logs = [
                log for log in door_logs if (
                    search_term in log["username"].lower() or
                    search_term in log["accountType"].lower() or
                    search_term in log["position"].lower() or
                    search_term in log["date"].isoformat().lower() or
                    search_term in log["time"].isoformat().lower() or
                    search_term in log["action_taken"].lower() 
                )
            ]
        else:
            filtered_logs = door_logs

    except Exception as e:
        filtered_logs = []
        print(f"Database error: {e}")
    finally:
        cursor.close()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('doorlogs_table_rows.html', door_logs=filtered_logs)

    return render_template('doorlogs.html', door_logs=filtered_logs)


@app.route('/notification')
def notification():
    return render_template('notification.html')

@app.route('/accounts')
def accounts():
    return render_template('accounts.html')


if __name__ == '__main__':
    app.run(debug=True)
