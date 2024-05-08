
from datetime import timedelta, datetime
from flask import Flask, request


app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        session_id = request.form.get('sessionId')
        session_code = request.form.get('serviceCode')
        phone_number = request.form.get('phoneNumber')
        text = request.form.get('text')

        response = ""

        if text == "":
            response = "CON Karibu! \n Which service would you like to access? \n"
            response += "1. List all buses \n"
            response += "2. Check ticket status \n"
            response += "3. Book a bus seat \n"
            response += "4. Cancel a booking \n"
            response += "5. Report an issue"

        elif text == "1":
            results = Bus.query.all()
            for i in results:
                response += f"END {i}: {i.is_available} {i.num_plate} \n \n"

        elif text == "2":
            response = "CON Choose an option \n"
            response += "1. All tickets \n"
            response += "2. Today active tickets"

        elif text == '2*1':
            tickets = Booking.query.filter_by(customer=phone_number).all()
            for tkt in tickets:
                response += f"END Ticket {tkt.id} on {tkt.departure:%Y-%m-%d %H:%M:%S}"

        elif text == '2*2':
            now = datetime.utcnow()
            tickets = Booking.query.filter_by(customer=phone_number, departure=now).all()

            if tickets:
                for tkt in tickets:
                    response += f"END Ticket {tkt.id} on {tkt.departure:%Y-%m-%d %H:%M:%S}"
            else:
                response = 'END No tickets found'

        elif text == '3':
            response = "CON Okay, pick a route \n"
            response += "1. Nairobi-Makongeni \n"
            response += "2. Nairobi-Thika \n"
            response += "3. Nairobi-Juja \n"
            response += "4. Nairobi-Kikuyu \n"
            response += "5. Nairobi-Kitengela"

        elif text == '3*1' or text == '3*2' or text == '3*3' or text == '3*4' or text == '3*5':
            # assuming each bus has a capacity of 37 seats
            seat = random.randint(1, 37)
            buses = Bus.query.filter_by(is_available=True).all()

            if buses:
                bus = buses[0]
                departure = datetime.utcnow() + timedelta(hours=1)
                # available_seats = bus.seats
                # check if there are available seats
                if bus.seats > 0:
                    new_booking = Booking(bus=bus, customer=phone_number, seat=seat, departure=departure)
                    db.session.add(new_booking)
                    bus.seats -= 1
                    db.session.commit()
                    response = f"END Here is your booking info: \n TICKET NO {new_booking.id} \n Bus Number is {bus} \n Your seat number is {seat} \n Your bus leaves at {departure:%H:%M:%S}"

                    # check if all seats are booked
                    if bus.seats == 0:
                        bus.is_available = False
                        db.session.commit()
                else:
                    response = "END Sorry, no seats available on this bus."
            else:
                response = "END No buses available for this route."

        elif text == "4":
            response = "END Work in progress, check again soon"
        elif text == "5":
            response = "END Work in progress, check again soon"

        return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)