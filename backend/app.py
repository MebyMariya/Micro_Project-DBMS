from flask import Flask, request
from flask_restful import Resource, Api
import mysql.connector

app = Flask(__name__)
api = Api(app)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="sqluser",
    password="1234",
    database="airline"
)
cursor = db.cursor()

class FlightListResource(Resource):
    def get(self):
        cursor.execute("SELECT * FROM flights")
        flights = cursor.fetchall()
        return {"flights": flights}

    def post(self):
        data = request.get_json()
        query = "INSERT INTO flights (flight_number, departure_airport, destination_airport, departure_date, available_seats) VALUES (%s, %s, %s, %s, %s)"
        values = (
            data["flight_number"],
            data["departure_airport"],
            data["destination_airport"],
            data["departure_date"],
            data["available_seats"]
        )
        cursor.execute(query, values)
        db.commit()
        return {"message": "Flight added successfully"}

class FlightResource(Resource):
    def get(self, flight_id):
        query = "SELECT * FROM flights WHERE id = %s"
        cursor.execute(query, (flight_id,))
        flight = cursor.fetchone()
        if flight:
            return {"flight": flight}
        else:
            return {"message": "Flight not found"}, 404

    def put(self, flight_id):
        data = request.get_json()
        query = "UPDATE flights SET flight_number=%s, departure_airport=%s, destination_airport=%s, departure_date=%s, available_seats=%s WHERE id=%s"
        values = (
            data["flight_number"],
            data["departure_airport"],
            data["destination_airport"],
            data["departure_date"],
            data["available_seats"],
            flight_id
        )
        cursor.execute(query, values)
        db.commit()
        return {"message": "Flight updated successfully"}

    def delete(self, flight_id):
        query = "DELETE FROM flights WHERE id = %s"
        cursor.execute(query, (flight_id,))
        db.commit()
        return {"message": "Flight deleted successfully"}

api.add_resource(FlightListResource, '/flights')
api.add_resource(FlightResource, '/flights/<int:flight_id>')

if __name__ == '__main__':
    app.run(debug=True)

