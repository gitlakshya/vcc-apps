"""
Service A - VCC-1 Microservice
Educational Purpose: Demonstrates inter-service communication in microservices architecture
Communicates with Service B at hardcoded IP address
"""

from flask import Flask, jsonify
import requests
import socket

app = Flask(__name__)

# Hardcoded IP address and port of Service B (vcc-2)
SERVICE_B_IP = "192.168.1.11"
SERVICE_B_PORT = 5002
SERVICE_B_URL = f"http://{SERVICE_B_IP}:{SERVICE_B_PORT}"

# Service A information
SERVICE_A_NAME = "Service-A-VCC-1"
SERVICE_A_PORT = 5001


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": SERVICE_A_NAME,
        "message": "Service A is running"
    }), 200


@app.route('/info', methods=['GET'])
def info():
    """Get service information"""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    return jsonify({
        "service_name": SERVICE_A_NAME,
        "service_port": SERVICE_A_PORT,
        "hostname": hostname,
        "local_ip": local_ip,
        "message": "This is Service A running on VCC-1"
    }), 200


@app.route('/call-service-b', methods=['GET'])
def call_service_b():
    """Call Service B and return its response"""
    try:
        # Attempt to call Service B
        response = requests.get(f"{SERVICE_B_URL}/response", timeout=5)
        
        if response.status_code == 200:
            service_b_data = response.json()
            return jsonify({
                "caller": SERVICE_A_NAME,
                "caller_port": SERVICE_A_PORT,
                "message": "Successfully called Service B",
                "service_b_response": service_b_data
            }), 200
        else:
            return jsonify({
                "caller": SERVICE_A_NAME,
                "error": f"Service B returned status code {response.status_code}"
            }), response.status_code
    
    except requests.exceptions.Timeout:
        return jsonify({
            "caller": SERVICE_A_NAME,
            "error": f"Service B at {SERVICE_B_URL} did not respond (timeout)"
        }), 504
    
    except requests.exceptions.ConnectionError:
        return jsonify({
            "caller": SERVICE_A_NAME,
            "error": f"Cannot connect to Service B at {SERVICE_B_URL}. Ensure Service B is running and network is configured correctly."
        }), 503
    
    except Exception as e:
        return jsonify({
            "caller": SERVICE_A_NAME,
            "error": str(e)
        }), 500


@app.route('/', methods=['GET'])
def index():
    """Welcome endpoint"""
    return jsonify({
        "service": SERVICE_A_NAME,
        "description": "Microservice A running on VCC-1",
        "endpoints": {
            "/": "Welcome message",
            "/health": "Health check",
            "/info": "Service information",
            "/call-service-b": "Call Service B at hardcoded IP"
        },
        "hardcoded_service_b": {
            "ip": SERVICE_B_IP,
            "port": SERVICE_B_PORT
        }
    }), 200


if __name__ == '__main__':
    print(f"Starting {SERVICE_A_NAME}...")
    print(f"Service A will run on port {SERVICE_A_PORT}")
    print(f"Service B (vcc-2) hardcoded at {SERVICE_B_IP}:{SERVICE_B_PORT}")
    app.run(host='0.0.0.0', port=SERVICE_A_PORT, debug=True)
