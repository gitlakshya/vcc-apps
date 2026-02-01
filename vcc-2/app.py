"""
Availability Service (Hotel Rooms) - VCC-2
Provides hotel room availability and pricing information
This service checks available rooms and pricing for hotel bookings
Educational Purpose: Learning how microservices expose domain-specific data
"""

import socket
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Service Configuration
SERVICE_NAME = "Availability"
SERVICE_PORT = 5002

# Mock hotel database (hardcoded for demonstration)
HOTELS_DATABASE = {
    "Grand Plaza": {
        "city": "New York",
        "rooms": {
            "Standard": {"available": 5, "rate": 120.00},
            "Deluxe": {"available": 3, "rate": 180.00},
            "Suite": {"available": 1, "rate": 300.00}
        }
    },
    "Oceanview Resort": {
        "city": "Miami",
        "rooms": {
            "Standard": {"available": 8, "rate": 100.00},
            "Deluxe": {"available": 4, "rate": 160.00},
            "Suite": {"available": 2, "rate": 280.00}
        }
    },
    "City Center Inn": {
        "city": "Chicago",
        "rooms": {
            "Standard": {"available": 2, "rate": 110.00},
            "Deluxe": {"available": 6, "rate": 170.00},
            "Suite": {"available": 0, "rate": 290.00}
        }
    }
}

def get_local_ip():
    """Get the local IP address of the service"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return "127.0.0.1"

def calculate_nights(check_in_str, check_out_str):
    """Calculate number of nights between check-in and check-out"""
    try:
        check_in = datetime.strptime(check_in_str, "%Y-%m-%d")
        check_out = datetime.strptime(check_out_str, "%Y-%m-%d")
        nights = (check_out - check_in).days
        return max(1, nights)
    except Exception as e:
        return 1

@app.route('/', methods=['GET'])
def welcome():
    """Welcome endpoint with service information"""
    return jsonify({
        "port": SERVICE_PORT,
        "description": "Hotel Room Availability Service",
        "endpoints": {
            "POST /check-availability": "Check hotel room availability and pricing",
            "GET /hotels": "List all available hotels"
        }
    })

@app.route('/hotels', methods=['GET'])
def list_hotels():
    """List all available hotels in the system"""
    hotels_list = []
    for hotel_name, hotel_info in HOTELS_DATABASE.items():
        hotels_list.append({
            "name": hotel_name,
            "city": hotel_info.get("city"),
            "room_types": list(hotel_info.get("rooms", {}).keys())
        })
    
    return jsonify({
        "status": "success",
        "available_hotels": hotels_list
    })

@app.route('/check-availability', methods=['POST'])
def check_availability():
    """
    Check hotel room availability and pricing
    Expected payload:
    {
        "hotel_name": "Grand Plaza",
        "check_in": "2026-02-15",
        "check_out": "2026-02-18",
        "room_type": "Deluxe",
        "num_guests": 2
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["hotel_name", "check_in", "check_out", "room_type"]
        if not all(field in data for field in required_fields):
            return jsonify({
                "status": "error",
                "message": "Missing required fields",
                "required_fields": required_fields
            }), 400
        
        hotel_name = data.get("hotel_name")
        room_type = data.get("room_type")
        check_in = data.get("check_in")
        check_out = data.get("check_out")
        num_guests = data.get("num_guests", 1)
        
        # Check if hotel exists
        if hotel_name not in HOTELS_DATABASE:
            return jsonify({
                "status": "not_found",
                "available": False,
                "message": f"Hotel '{hotel_name}' not found in system",
                "available_hotels": list(HOTELS_DATABASE.keys())
            }), 404
        
        hotel = HOTELS_DATABASE[hotel_name]
        
        # Check if room type exists for this hotel
        if room_type not in hotel.get("rooms", {}):
            return jsonify({
                "status": "not_found",
                "available": False,
                "message": f"Room type '{room_type}' not available at {hotel_name}",
                "available_room_types": list(hotel.get("rooms", {}).keys())
            }), 404
        
        room_info = hotel["rooms"][room_type]
        available_count = room_info.get("available", 0)
        room_rate = room_info.get("rate", 0)
        
        # Calculate number of nights
        num_nights = calculate_nights(check_in, check_out)
        
        # Check if room is available
        if available_count < 1:
            return jsonify({
                "status": "unavailable",
                "available": False,
                "hotel_name": hotel_name,
                "room_type": room_type,
                "check_in": check_in,
                "check_out": check_out,
                "message": f"No {room_type} rooms available for the selected dates"
            }), 200
        
        # Room is available - return details
        total_price = room_rate * num_nights
        
        return jsonify({
            "status": "success",
            "available": True,
            "hotel_name": hotel_name,
            "city": hotel.get("city"),
            "room_type": room_type,
            "check_in": check_in,
            "check_out": check_out,
            "num_nights": num_nights,
            "num_guests": num_guests,
            "room_rate": room_rate,
            "total_price": total_price,
            "available_rooms": available_count,
            "currency": "USD",
            "timestamp": datetime.now().isoformat()
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Availability check error: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("Starting Availability Service (Hotel Rooms)...")
    print("=" * 60)
    print(f"Service: {SERVICE_NAME}")
    print(f"Port: {SERVICE_PORT}")
    print(f"Local IP: {get_local_ip()}")
    print(f"Hotels in database: {', '.join(HOTELS_DATABASE.keys())}")
    print("=" * 60)
    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=True)
