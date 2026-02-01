"""
Service B - VCC-2 Microservice
Educational Purpose: Demonstrates inter-service communication in microservices architecture
Responds to requests from Service A with hardcoded response strings
"""

from flask import Flask, jsonify
import socket

app = Flask(__name__)

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
        "data": { "This demonstration is for Educational Purpose only"
        }
    }), 200


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
            "/response": "Service B response (called by Service A)"
        }
    }), 200


if __name__ == '__main__':
    print(f"Starting {SERVICE_B_NAME}...")
    print(f"Service B will run on port {SERVICE_B_PORT}")
    app.run(host='0.0.0.0', port=SERVICE_B_PORT, debug=True)
