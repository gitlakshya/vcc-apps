"""
Payment Service (Hotel Booking) - VCC-3
Demonstrates payment processing in a microservices hotel booking workflow
This service processes hotel booking payments with mock payment gateway logic
Educational Purpose: Learning inter-service communication patterns
"""

import socket
import json
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Service Configuration
SERVICE_NAME = "Payment"
SERVICE_PORT = 5003
SERVICE_A_IP = "10.109.0.150"
SERVICE_A_PORT = 5001

# Mock payment database
PAYMENT_TRANSACTIONS = {}
TRANSACTION_COUNTER = 1000

# Mock payment processing rules (hardcoded for demonstration)
VALID_PAYMENT_METHODS = ["credit_card", "debit_card", "bank_transfer"]
PAYMENT_SUCCESS_RATE = 0.95  # 95% of payments succeed

def get_local_ip():
    """Get the local IP address of the service"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

@app.route('/', methods=['GET'])
def welcome():
    """Welcome endpoint with service information"""
    return jsonify({
        "port": SERVICE_PORT,
        "description": "Hotel Booking Payment Processing Service",
        "endpoints": {
            "POST /process-payment": "Process payment for hotel booking",
            "GET /payment-status/<transaction_id>": "Check payment status"
        }
    })

@app.route('/process-payment', methods=['POST'])
def process_payment():
    """
    Process payment for hotel booking
    Expected payload:
    {
        "booking_id": "BOOK123",
        "guest_name": "John Doe",
        "hotel_name": "Grand Plaza",
        "room_type": "Deluxe",
        "amount": 350.00,
        "currency": "USD",
        "payment_method": "credit_card",
        "check_in": "2026-02-15",
        "check_out": "2026-02-18"
    }
    """
    global TRANSACTION_COUNTER
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["booking_id", "guest_name", "hotel_name", "amount", "payment_method"]
        if not all(field in data for field in required_fields):
            return jsonify({
                "status": "error",
                "message": "Missing required payment fields",
                "required_fields": required_fields
            }), 400
        
        # Validate payment method
        if data.get("payment_method") not in VALID_PAYMENT_METHODS:
            return jsonify({
                "status": "failed",
                "message": f"Invalid payment method. Accepted: {', '.join(VALID_PAYMENT_METHODS)}",
                "transaction_id": None
            }), 400
        
        # Validate amount
        if data.get("amount", 0) <= 0:
            return jsonify({
                "status": "failed",
                "message": "Invalid payment amount. Amount must be greater than 0",
                "transaction_id": None
            }), 400
        
        # Generate transaction ID
        TRANSACTION_COUNTER += 1
        transaction_id = f"TXN{TRANSACTION_COUNTER}"
        
        # Simulate payment processing (hardcoded rules for demonstration)
        # In real scenario: call actual payment gateway
        amount = data.get("amount", 0)
        
        # Decline payments over $10,000 or with suspicious patterns
        if amount > 10000:
            payment_status = "declined"
            reason = "Amount exceeds maximum limit"
        elif "xxx" in data.get("payment_method", "").lower():
            payment_status = "declined"
            reason = "Invalid payment method detected"
        else:
            # Random success for demonstration
            import random
            payment_status = "approved" if random.random() < PAYMENT_SUCCESS_RATE else "declined"
            reason = "Payment gateway approval" if payment_status == "approved" else "Insufficient funds"
        
        # Store transaction
        transaction = {
            "transaction_id": transaction_id,
            "booking_id": data.get("booking_id"),
            "guest_name": data.get("guest_name"),
            "hotel_name": data.get("hotel_name"),
            "room_type": data.get("room_type", "Standard"),
            "amount": amount,
            "currency": data.get("currency", "USD"),
            "payment_method": data.get("payment_method"),
            "status": payment_status,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
            "check_in": data.get("check_in"),
            "check_out": data.get("check_out")
        }
        
        PAYMENT_TRANSACTIONS[transaction_id] = transaction
        
        # Return response
        if payment_status == "approved":
            return jsonify({
                "status": "success",
                "message": "Payment processed successfully",
                "transaction_id": transaction_id,
                "booking_id": data.get("booking_id"),
                "amount": amount,
                "currency": data.get("currency", "USD"),
                "payment_status": payment_status,
                "hotel_name": data.get("hotel_name"),
                "guest_name": data.get("guest_name"),
                "timestamp": transaction["timestamp"]
            }), 200
        else:
            return jsonify({
                "status": "failed",
                "message": f"Payment declined: {reason}",
                "transaction_id": transaction_id,
                "booking_id": data.get("booking_id"),
                "amount": amount
            }), 402

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Payment processing error: {str(e)}"
        }), 500

@app.route('/payment-status/<transaction_id>', methods=['GET'])
def payment_status(transaction_id):
    """Get the status of a payment transaction"""
    if transaction_id not in PAYMENT_TRANSACTIONS:
        return jsonify({
            "status": "not_found",
            "message": f"Transaction {transaction_id} not found",
            "transaction_id": transaction_id
        }), 404
    
    transaction = PAYMENT_TRANSACTIONS[transaction_id]
    return jsonify({
        "status": "success",
        "transaction_id": transaction_id,
        "booking_id": transaction.get("booking_id"),
        "guest_name": transaction.get("guest_name"),
        "hotel_name": transaction.get("hotel_name"),
        "amount": transaction.get("amount"),
        "currency": transaction.get("currency"),
        "payment_status": transaction.get("status"),
        "reason": transaction.get("reason"),
        "timestamp": transaction.get("timestamp")
    })

if __name__ == '__main__':
    print("=" * 60)
    print("Starting Payment Service (Hotel Booking)...")
    print("=" * 60)
    print(f"Service: {SERVICE_NAME}")
    print(f"Port: {SERVICE_PORT}")
    print(f"Local IP: {get_local_ip()}")
    print(f"Endpoints: /process-payment, /payment-status/<txn_id>")
    print("=" * 60)
    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=True)
