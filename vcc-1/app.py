"""
Orchestrator (Hotel Booking) - VCC-1
Orchestrates hotel booking workflow across multiple microservices
This service accepts booking requests and coordinates with availability and payment services
Educational Purpose: Learning service orchestration patterns in microservices
"""

import socket
import requests
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Service Configuration
SERVICE_NAME = "Orchestrator"
SERVICE_PORT = 5001

# Downstream services configuration
SERVICE_B_IP = "10.109.0.151"
SERVICE_B_PORT = 5002
SERVICE_C_IP = "10.109.0.152"
SERVICE_C_PORT = 5003

REQUEST_TIMEOUT = 5

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

@app.route('/', methods=['GET'])
def welcome():
    """Welcome endpoint with service information"""
    return jsonify({
        "port": SERVICE_PORT,
        "description": "Hotel Booking Orchestrator Service",
        "endpoints": {
            "POST /book-hotel": "Book a hotel (orchestrates availability and payment)"
        }
    })

@app.route('/book-hotel', methods=['POST'])
def book_hotel():
    """
    Orchestrate hotel booking workflow with hardcoded values
    Flow: 1. Check availability with Availability Service
          2. If available, process payment with Payment Service
          3. Return consolidated booking confirmation
    """
    try:
        # Hardcoded booking details
        guest_name = "Lakshya Vashisth"
        guest_email = "lakshya@example.com"
        hotel_name = "Grand Plaza"
        check_in = "2026-02-15"
        check_out = "2026-02-18"
        room_type = "Suite"
        payment_method = "credit_card"
        num_guests = 1
        
        booking_id = f"BOOK{int(datetime.now().timestamp())}"
        
        # Step 1: Check availability with Availability Service
        print(f"[{SERVICE_NAME}] Checking availability...")
        try:
            availability_response = requests.post(
                f"http://{SERVICE_B_IP}:{SERVICE_B_PORT}/check-availability",
                json={
                    "hotel_name": hotel_name,
                    "check_in": check_in,
                    "check_out": check_out,
                    "room_type": room_type,
                    "num_guests": num_guests
                },
                timeout=REQUEST_TIMEOUT
            )
            
            if availability_response.status_code != 200:
                return jsonify({
                    "status": "booking_failed",
                    "message": "Hotel availability service unavailable",
                    "booking_id": booking_id
                }), 503
            
            availability_data = availability_response.json()
            
            # Check if room is available
            if availability_data.get("available") is False:
                return jsonify({
                    "status": "booking_failed",
                    "message": f"No {room_type} rooms available at {hotel_name} for selected dates",
                    "booking_id": booking_id,
                    "check_in": check_in,
                    "check_out": check_out
                }), 409
            
            room_rate = availability_data.get("room_rate", 0)
            num_nights = availability_data.get("num_nights", 0)
            total_amount = room_rate * num_nights
            
        except requests.exceptions.Timeout:
            return jsonify({
                "status": "error",
                "message": "Availability service timeout",
                "booking_id": booking_id
            }), 504
        except requests.exceptions.ConnectionError:
            return jsonify({
                "status": "error",
                "message": f"Cannot connect to availability service at {SERVICE_B_IP}:{SERVICE_B_PORT}",
                "booking_id": booking_id
            }), 503
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Availability check error: {str(e)}",
                "booking_id": booking_id
            }), 500
        
        # Step 2: Process payment with Payment Service
        print(f"[{SERVICE_NAME}] Processing payment...")
        try:
            payment_response = requests.post(
                f"http://{SERVICE_C_IP}:{SERVICE_C_PORT}/process-payment",
                json={
                    "booking_id": booking_id,
                    "guest_name": guest_name,
                    "hotel_name": hotel_name,
                    "room_type": room_type,
                    "amount": total_amount,
                    "currency": "USD",
                    "payment_method": payment_method,
                    "check_in": check_in,
                    "check_out": check_out
                },
                timeout=REQUEST_TIMEOUT
            )
            
            payment_data = payment_response.json()
            
            if payment_response.status_code not in [200, 201]:
                return jsonify({
                    "status": "booking_failed",
                    "message": payment_data.get("message", "Payment processing failed"),
                    "booking_id": booking_id,
                    "reason": "Payment declined"
                }), 402
            
        except requests.exceptions.Timeout:
            return jsonify({
                "status": "error",
                "message": "Payment service timeout",
                "booking_id": booking_id
            }), 504
        except requests.exceptions.ConnectionError:
            return jsonify({
                "status": "error",
                "message": f"Cannot connect to payment service at {SERVICE_C_IP}:{SERVICE_C_PORT}",
                "booking_id": booking_id
            }), 503
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Payment processing error: {str(e)}",
                "booking_id": booking_id
            }), 500
        
        # Step 3: Return consolidated booking confirmation
        transaction_id = payment_data.get("transaction_id")
        
        booking_confirmation = {
            "status": "confirmed",
            "message": "Hotel booking confirmed successfully",
            "booking_id": booking_id,
            "transaction_id": transaction_id,
            "guest_name": guest_name,
            "guest_email": guest_email,
            "hotel_name": hotel_name,
            "room_type": room_type,
            "check_in": check_in,
            "check_out": check_out,
            "number_of_nights": num_nights,
            "room_rate_per_night": room_rate,
            "total_amount": total_amount,
            "currency": "USD",
            "payment_status": "approved",
            "booking_timestamp": datetime.now().isoformat()
        }
        
        return jsonify(booking_confirmation), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Booking orchestration error: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("Starting Orchestrator (Hotel Booking)...")
    print("=" * 60)
    print(f"Service: {SERVICE_NAME}")
    print(f"Port: {SERVICE_PORT}")
    print(f"Local IP: {get_local_ip()}")
    print(f"Availability Service: {SERVICE_B_IP}:{SERVICE_B_PORT}")
    print(f"Payment Service: {SERVICE_C_IP}:{SERVICE_C_PORT}")
    print("=" * 60)
    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=True)
