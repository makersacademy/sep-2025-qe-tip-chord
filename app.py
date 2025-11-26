import os
from flask import Flask, request, render_template, redirect, url_for
from lib.database_connection import get_flask_database_connection
from lib.gig_repository import GigRepository
from lib.gig import Gig
from lib.booking_repository import BookingRepository
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import datetime
import json

app = Flask(__name__)
app.config.update(
    SECRET_KEY="adobgaiodbgaidgbiodgb",
)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def signed_up(self, connection, username):
        rows = connection.execute('SELECT * FROM users WHERE username = %s', [username])
        return len(rows) > 0
    def password_valid(self, connection, username, password_attempt):
        if not self.signed_up(connection, username):
            return False
        rows = connection.execute('SELECT * FROM users WHERE username = %s', [username])
        return check_password_hash(rows[0]["hashed_password"], password_attempt)
    def get_user_database_id(self, connection, username):
        rows = connection.execute('SELECT * FROM users WHERE username = %s', [username])
        return rows[0]["id"]
    def get_username(self, connection, id):
        rows = connection.execute('SELECT * FROM users WHERE id = %s', [id])
        return rows[0]["username"]
    def sign_up(self, connection, username, password):
        hashed_password = generate_password_hash(password)
        connection.execute('INSERT INTO users (username, hashed_password) VALUES (%s, %s)', [username, hashed_password])

@login_manager.user_loader
def user_loader(username: str):
    connection = get_flask_database_connection(app)
    if User().signed_up(connection, username):
        user_model = User()
        user_model.id = username
        return user_model
    return None

def admin_user_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.__dict__.get("id") and current_user.id == "admin":
            return func(*args, **kwargs)
        else:
            return redirect(url_for('get_home'))
    return decorated_view

@app.errorhandler(401)
def unauthorised(e):
    return render_template('401.html'), 401

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



@app.route('/', methods=['GET'])
def get_root():
    return redirect(url_for('get_home'))

@app.route('/home', methods=['GET'])
def get_home():
    logged_in_as = ", " + str(current_user.id) if current_user.__dict__.get("id") else None
    return render_template('home.html', logged_in_as=logged_in_as)

@app.route('/about', methods=['GET'])
def get_about():
    logged_in_as = ", " + str(current_user.id) if current_user.__dict__.get("id") else None
    return render_template('about.html', logged_in_as=logged_in_as)

@app.route('/gigs', methods=['GET', 'POST'])
def get_gigs():
    connection = get_flask_database_connection(app)
    repo = GigRepository(connection)
    venue_locations = [("", "All")]
    for gig in repo.all():
        if (gig.venue, gig.location) not in venue_locations:
            venue_locations.append((gig.venue, gig.location))
    locations = [vl[1] for vl in venue_locations]
    selected_location = "All"
    if "location" in request.form.keys():
        selected_location = request.form["location"]
    date_from = datetime.datetime.now().strftime("%Y-%m-%d")
    if "date_from" in request.form.keys() and request.form["date_from"]:
        date_from = request.form["date_from"]
    date_to = (datetime.datetime.now() + datetime.timedelta(weeks=+4)).strftime("%Y-%m-%d")
    if "date_to" in request.form.keys() and request.form["date_to"]:
        date_to = request.form["date_to"]
    gigs = repo.get_by_location_and_dates(selected_location, date_from, date_to)
    logged_in_as = ", " + str(current_user.id) if current_user.__dict__.get("id") else None
    return render_template('gigs.html', gigs=gigs, locations=locations, selected_location=selected_location, date_from=date_from, date_to=date_to, logged_in_as=logged_in_as)

@app.route('/gigs/<id>', methods=['GET'])
def get_gig_by_id(id):
    connection = get_flask_database_connection(app)
    repo = GigRepository(connection)
    gig = repo.get_by_id(id)
    logged_in_as = str(current_user.id) if current_user.__dict__.get("id") else None
    repo = BookingRepository(connection)
    if current_user.__dict__ != {}:
        user_database_id = User().get_user_database_id(connection, current_user.id)
        already_booked_gig = gig.id in [booking.gig_id for booking in repo.get_bookings(user_database_id)]
    else:
        already_booked_gig = False
    gig_in_past = gig.datetime < datetime.datetime.now()
    return render_template('gig.html', gig=gig, logged_in_as=logged_in_as, already_booked_gig=already_booked_gig, gig_in_past=gig_in_past)

@app.route('/bands/<band_name>', methods=["GET"])
def get_band_by_name(band_name):
    connection = get_flask_database_connection(app)
    repo = GigRepository(connection)
    gigs = repo.get_by_band_name(band_name)
    logged_in_as = ", " + str(current_user.id) if current_user.__dict__.get("id") else None
    return render_template('band.html', gigs=gigs, band_name=band_name, logged_in_as=logged_in_as)

@app.route('/book_gig/<gig_id>', methods=["POST"])
@login_required
def post_book_gig(gig_id):
    try:
        int(request.form["ticket_count"])
    except:
        return render_template('400.html', reason="Non-integer ticket number requested"), 400
    if int(request.form["ticket_count"]) < 1:
        return render_template('400.html', reason="Ticket number must be at least 1"), 400
    if int(request.form["ticket_count"]) > 8:
        return render_template('400.html', reason="A user can't book more than 8 tickets for one gig"), 400
    connection = get_flask_database_connection(app)
    repo = BookingRepository(connection)
    user_database_id = User().get_user_database_id(connection, current_user.id)
    repo.make_booking(gig_id, user_database_id, request.form["ticket_count"])
    return redirect(url_for('get_account'))

@app.route('/cancel_booking/<booking_id>', methods=["GET"])
@login_required
def get_cancel_booking(booking_id):
    connection = get_flask_database_connection(app)
    repo = BookingRepository(connection)
    repo.cancel_booking(booking_id)
    return redirect(url_for('get_account'))

@app.route('/login', methods=["POST"])
def post_login():
    username = request.form["username"]
    password = request.form["password"]
    connection = get_flask_database_connection(app)

    if User().signed_up(connection, username):
        if User().password_valid(connection, username, password):
            user_model = User()
            user_model.id = username
            login_user(user_model)
            return redirect(url_for('get_home'))
        else:
            return render_template('401.html', reason="Wrong credentials"), 401
    return render_template('401.html', reason="Unknown user"), 401

@app.route('/login', methods=['GET'])
def get_login():
    signup_message = None
    if "signup_message" in request.args.keys():
        signup_message = request.args["signup_message"]
    logged_in_as = ", " + str(current_user.id) if current_user.__dict__.get("id") else None
    return render_template('login.html', logged_in_as=logged_in_as, signup_message=signup_message)

def password_complexity(password):
    return len(password) > 7 and any(char in password for char in "!@$%&")

@app.route('/signup', methods=['GET', 'POST'])
def get_signup():
    logged_in_as = ", " + str(current_user.id) if current_user.__dict__.get("id") else None
    if logged_in_as:
        return redirect(url_for('get_home'))
    username_error = None
    password_error = None
    username = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if password != confirm_password:
            password_error = "Passwords did not match"
        elif not password_complexity(password):
            password_error = "Password complexity requirements not met"
        elif username == "":
            username_error = "Username cannot be blank"
        elif username.lower() == "admin":
            username_error = "Username cannot be 'admin' (or similar)"
        if not username_error and not password_error:
            connection = get_flask_database_connection(app)
            User().sign_up(connection, username, password)
            return redirect(url_for('get_login', signup_message=[True]))
    return render_template('signup.html', username_error=username_error, password_error=password_error, username=username)

@app.route('/logout', methods=['GET'])
def get_logout():
    logout_user()
    return render_template('logout.html')

@app.route('/account', methods=['GET'])
@login_required
def get_account():
    connection = get_flask_database_connection(app)
    repo = BookingRepository(connection)
    user_database_id = User().get_user_database_id(connection, current_user.id)
    bookings = repo.get_bookings(user_database_id)
    repo = GigRepository(connection)
    gigs = repo.all()
    booking_details = []
    for booking in bookings:
        ticket_text = f"{booking.ticket_count} tickets" if booking.ticket_count > 1 else f"{booking.ticket_count} ticket"
        booking_details.append({
            "ticket_count": ticket_text,
            "gig": repo.get_by_id(booking.gig_id),
            "id": booking.id
        })
    logged_in_as = ", " + str(current_user.id) if current_user.__dict__.get("id") else None
    return render_template('account.html', booking_details=booking_details, logged_in_as=logged_in_as)



# Admin routes

@app.route('/admin', methods=["GET"])
@admin_user_required
def get_admin():
    logged_in_as = ", " + str(current_user.id) if current_user.__dict__.get("id") else None
    return render_template('admin.html', logged_in_as=logged_in_as)

@app.route('/admin_add_gig', methods=["POST"])
@admin_user_required
def admin_add_gig():
    connection = get_flask_database_connection(app)
    repo = GigRepository(connection)
    datetime = request.form["datetime"]
    band = request.form["band"]
    venue = request.form["venue"]
    location = request.form["location"]
    postcode = request.form["postcode"]
    repo.add_gig(Gig(None, datetime, band, venue, location, postcode))
    return render_template('admin.html')



# API routes

@app.route('/api')
def api_root():
    return "Specify a resource such as \"gigs\" via a request like GET /api/&lt;resource&gt;"

@app.route('/api/<resource>')
def api_resource(resource):
    match resource:
        case "gigs":
            if request.method == "GET":
                selected_location = "All"
                if "location" in request.args.keys():
                    selected_location = request.args["location"]
                date_from = datetime.datetime.now().strftime("%Y-%m-%d")
                if "date_from" in request.args.keys():
                    date_from = request.args["date_from"]
                date_to = (datetime.datetime.now() + datetime.timedelta(weeks=+4)).strftime("%Y-%m-%d")
                if "date_to" in request.args.keys():
                    date_to = request.args["date_to"]
                connection = get_flask_database_connection(app)
                repo = GigRepository(connection)
                gigs = repo.get_by_location_and_dates(selected_location, date_from, date_to)
                return json.dumps([gig.jsonify() for gig in gigs])
        case "bands":
            if request.method == "GET":
                connection = get_flask_database_connection(app)
                repo = GigRepository(connection)
                gigs = repo.all()
                bands = set([gig.band for gig in gigs])
                return json.dumps(list(bands))
        case "accounts" | "bookings":
            return "Specify an Id for this resource via a request like GET /api/&lt;resource&gt;/&lt;Id&gt;"
        case _:
            return "Unknown API resource: " + resource, 404

@app.route('/api/gigs/<id>')
def api_gig(id):
    connection = get_flask_database_connection(app)
    repo = GigRepository(connection)
    gig = repo.get_by_id(id)
    try:
        return json.dumps(gig.jsonify())
    except:
        return json.dumps({}), 404

@app.route('/api/bands/<name>')
def api_band(name):
    connection = get_flask_database_connection(app)
    repo = GigRepository(connection)
    gigs = repo.get_by_band_name(name)
    return json.dumps([gig.jsonify() for gig in gigs])

@app.route('/api/accounts/<id>')
@login_required
def api_account(id):
    connection = get_flask_database_connection(app)
    repo = BookingRepository(connection)
    bookings = repo.get_bookings(id)
    try:
        username = User().get_username(connection, id)
        return json.dumps({
            "bookings": [booking.jsonify() for booking in bookings],
            "username": username
        })
    except:
        return json.dumps({}), 404

@app.route('/api/bookings/<id>', methods=["GET"])
@admin_user_required
def api_booking(id):
    connection = get_flask_database_connection(app)
    repo = BookingRepository(connection)
    booking = repo.get_by_id(id)
    try:
        return json.dumps(booking.jsonify())
    except:
        return json.dumps({}), 404

@app.route('/api/bookings', methods=["POST"])
@admin_user_required
def api_post_booking():
    connection = get_flask_database_connection(app)
    repo = BookingRepository(connection)
    try:
        gig_id = request.form["gig_id"]
        user_id = request.form["user_id"]
        ticket_count = request.form["ticket_count"]
        repo.make_booking(gig_id, user_id, ticket_count)
        return "", 200
    except:
        return "POST failed", 400

@app.route('/api/bookings/<id>', methods=["DELETE"])
@admin_user_required
def api_delete_booking(id):
    connection = get_flask_database_connection(app)
    repo = BookingRepository(connection)
    booking = repo.cancel_booking(id)
    return "", 200

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
