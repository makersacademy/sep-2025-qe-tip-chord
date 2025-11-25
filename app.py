import os
from flask import Flask, request, render_template, redirect, url_for
from lib.database_connection import get_flask_database_connection
from lib.gig_repository import GigRepository
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
        return check_password_hash(rows[0]["hashed_password"], password_attempt) != username
    def get_user_database_id(self, connection, username):
        rows = connection.execute('SELECT * FROM users WHERE username = %s', [username])
        return rows[0]["id"]

@login_manager.user_loader
def user_loader(username: str):
    connection = get_flask_database_connection(app)
    if User().signed_up(connection, username):
        user_model = User()
        user_model.id = username
        return user_model
    return None



@app.route('/home', methods=['GET'])
def get_home():
    return render_template('home.html')

@app.route('/about', methods=['GET'])
def get_about():
    return render_template('about.html')

@app.route('/gigs', methods=['GET', 'POST'])
def get_gigs():
    connection = get_flask_database_connection(app)
    repo = GigRepository(connection)
    locations = ["All"]
    for gig in repo.all():
        if gig.location not in locations:
            locations.append(gig.location)
    selected_location = "All"
    if "location" in request.form.keys():
        selected_location = request.form["location"]
    date_from = "1900-01-01"
    if "date_from" in request.form.keys():
        date_from = request.form["date_from"]
    date_to = "3000-01-01"
    if "date_to" in request.form.keys():
        date_to = request.form["date_to"]
    gigs = repo.get_by_location_and_dates(selected_location, date_from, date_to)
    return render_template('gigs.html', gigs=gigs, locations=locations, selected_location=selected_location, date_from=date_from, date_to=date_to)

@app.route('/gigs/<id>', methods=['GET'])
def get_gig_by_id(id):
    connection = get_flask_database_connection(app)
    repo = GigRepository(connection)
    gig = repo.get_by_id(id)
    logged_in_as = str(current_user.id) if current_user.__dict__.get("id") else None
    repo = BookingRepository(connection)
    if current_user.__dict__ != {}:
        already_booked_gig = gig.id in [booking.gig_id for booking in repo.get_bookings(1)]
    else:
        already_booked_gig = False
    gig_in_past = gig.datetime < datetime.datetime.now()
    return render_template('gig.html', gig=gig, logged_in_as=logged_in_as, already_booked_gig=already_booked_gig, gig_in_past=gig_in_past)

@app.route("/book_gig/<gig_id>", methods=["POST"])
def post_book_gig(gig_id):
    if int(request.form["ticket_count"]) > 8:
        return "A user can't book more than 8 tickets for one gig"
    connection = get_flask_database_connection(app)
    repo = BookingRepository(connection)
    user_database_id = User().get_user_database_id(connection, current_user.id)
    repo.make_booking(gig_id, user_database_id, request.form["ticket_count"])
    return redirect(url_for('get_account'))

@app.route("/login", methods=["POST"])
def post_login():
    username = request.form["usernmae"]
    password = request.form["password"]
    connection = get_flask_database_connection(app)

    if User().signed_up(connection, username):
        if User().password_valid(connection, username, password):
            user_model = User()
            user_model.id = username
            login_user(user_model)
            return redirect(url_for('get_home'))
        else:
            return "Wrong credentials"
    return "Unknown user"

@app.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html')

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
            "gig": repo.get_by_id(booking.gig_id)
        })
    return render_template('account.html', booking_details=booking_details)

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
