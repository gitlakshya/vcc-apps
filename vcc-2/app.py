"""
Service B - VCC-2 Microservice
Educational Purpose: Demonstrates inter-service communication in microservices architecture
Responds to requests from Service A with hardcoded response strings
"""

from flask import Flask, jsonify
import requests
import socket

app = Flask(__name__)

# Hardcoded IP address and port of Service A (vcc-1)
SERVICE_A_IP = "10.109.0.150"
SERVICE_A_PORT = 5001
SERVICE_A_URL = f"http://{SERVICE_A_IP}:{SERVICE_A_PORT}"

# Service B information
SERVICE_B_NAME = "Service-B-VCC-2"
SERVICE_B_PORT = 5002


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": SERVICE_B_NAME,
        "message": "Service B is running"
    }), 200


@app.route('/info', methods=['GET'])
def info():
    """Get service information"""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    return jsonify({
        "service_name": SERVICE_B_NAME,
        "service_port": SERVICE_B_PORT,
        "hostname": hostname,
        "local_ip": local_ip,
        "message": "This is Service B running on VCC-2"
    }), 200


@app.route('/response', methods=['GET'])
def response():
    """Service B response endpoint - called by Service A"""
    return jsonify({
        "service_name": SERVICE_B_NAME,
        "port": SERVICE_B_PORT,
        "message": "This is a response from VCC-2 Micro Service",
        "data": {"purpose": "This demonstration is for Educational Purpose only"}
    }), 200


@app.route('/call-service-a', methods=['GET'])
def call_service_a():
    """Call Service A and return its response - demonstrates bidirectional communication"""
    try:
        # Attempt to call Service A
        response = requests.get(f"{SERVICE_A_URL}/info", timeout=5)
        
        if response.status_code == 200:
            service_a_data = response.json()
            return jsonify({
                "caller": SERVICE_B_NAME,
                "caller_port": SERVICE_B_PORT,
                "message": "Successfully called Service A",
                "service_a_response": service_a_data
            }), 200
        else:
            return jsonify({
                "caller": SERVICE_B_NAME,
                "error": f"Service A returned status code {response.status_code}"
            }), response.status_code
    
    except requests.exceptions.Timeout:
        return jsonify({
            "caller": SERVICE_B_NAME,
            "error": f"Service A at {SERVICE_A_URL} did not respond (timeout)"
        }), 504
    
    except requests.exceptions.ConnectionError:
        return jsonify({
            "caller": SERVICE_B_NAME,
            "error": f"Cannot connect to Service A at {SERVICE_A_URL}. Ensure Service A is running and network is configured correctly."
        }), 503
    
    except Exception as e:
        return jsonify({
            "caller": SERVICE_B_NAME,
            "error": str(e)
        }), 500


@app.route('/', methods=['GET'])
def index():
    """Welcome endpoint"""
    return jsonify({
        "service": SERVICE_B_NAME,
        "description": "Microservice B running on VCC-2",
        "endpoints": {
            "/": "Welcome message",
            "/health": "Health check",
            "/info": "Service information",
            "/response": "Service B response (called by Service A)",
            "/call-service-a": "Call Service A (bidirectional communication)"
        },
        "hardcoded_service_a": {
            "ip": SERVICE_A_IP,
            "port": SERVICE_A_PORT
        }
    }), 200


if __name__ == '__main__':
    print(f"Starting {SERVICE_B_NAME}...")
    print(f"Service B will run on port {SERVICE_B_PORT}")
    app.run(host='0.0.0.0', port=SERVICE_B_PORT, debug=True)
