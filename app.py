import os
from flask import Flask, request, render_template, redirect, url_for
from lib.database_connection import get_flask_database_connection
from lib.gig_repository import GigRepository
from lib.booking_repository import BookingRepository

app = Flask(__name__)

@app.route('/home', methods=['GET'])
def get_home():
    return render_template('home.html')

@app.route('/about', methods=['GET'])
def get_about():
    return render_template('about.html')

@app.route('/gigs', methods=['GET'])
def get_gigs():
    connection = get_flask_database_connection(app)
    repo = BookingRepository(connection)
    gig_booked_ids = [booking.gig_id for booking in repo.get_bookings()]
    repo = GigRepository(connection)
    gigs = repo.all()
    gig_ids = [gig.id for gig in gigs]
    booked_percentage = int(len(set(gig_booked_ids)) / len(set(gig_ids)) * 100)
    return render_template('gigs.html', gigs=gigs, number_bookings=booked_percentage)

@app.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def get_logout():
    return render_template('logout.html')

@app.route('/account', methods=['GET'])
def get_account():
    connection = get_flask_database_connection(app)
    repo = BookingRepository(connection)
    bookings = repo.get_bookings()
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

@app.route('/tcs', methods=['GET'])
def get_tcs():
    return render_template('tcs.html')

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
