# Multi-VM Microservices Project

## 📋 Project Overview

This project demonstrates a practical implementation of microservices architecture using VirtualBox Virtual Machines. Two Flask-based microservices communicate with each other across a host-only network with hardcoded IP addresses for educational purposes.

**Project Status:** Educational - For Learning Purposes  
**Last Updated:** February 1, 2026

---

## 🎯 Project Objectives

1. **Create and configure multiple Virtual Machines (VMs)** using VirtualBox
2. **Establish network communication** between VMs on a host-only network
3. **Deploy microservices** across the connected VMs
4. **Demonstrate inter-service communication** with hardcoded IP addresses
5. **Document the complete implementation** with setup guides and architecture diagrams

---

## 📦 Deliverables

### 1. **Source Code Repository**
This repository contains:
- ✅ `vcc-1/app.py` - Orchestrator microservice code
- ✅ `vcc-1/requirements.txt` - Dependencies for Orchestrator
- ✅ `vcc-2/app.py` - Availability microservice code
- ✅ `vcc-2/requirements.txt` - Dependencies for Availability
- ✅ `vcc-3/app.py` - Payment microservice code
- ✅ `vcc-3/requirements.txt` - Dependencies for Payment
- ✅ `VIRTUALBOX_SETUP_GUIDE.md` - Complete VirtualBox setup instructions
- ✅ `ARCHITECTURE_DESIGN.md` - Architecture diagrams and design documentation
- ✅ `DEPLOYMENT_INSTRUCTIONS.md` - Step-by-step deployment guide
- ✅ `README.md` - This file
- ✅ `PLAGIARISM_CLAUSE.md` - Academic integrity statement

### 2. **Step-by-Step Implementation Guide**
See `VIRTUALBOX_SETUP_GUIDE.md` for:
- VirtualBox installation on different operating systems
- VM creation and configuration
- Network setup and static IP assignment
- Service deployment procedures

### 3. **Architecture Design Documentation**
See `ARCHITECTURE_DESIGN.md` for:
- System architecture diagrams (ASCII format)
- Component specifications
- Network flow visualization
- Deployment layer diagrams
- Production considerations

### 4. **Deployment & Testing Documentation**
See `DEPLOYMENT_INSTRUCTIONS.md` for:
- Pre-deployment checklist
- Service deployment procedures
- Verification and testing steps
- Monitoring and logging
- Troubleshooting guide

---

## 🏗️ System Architecture

### High-Level Overview

```
VirtualBox Host-only Network (10.109.0.0/23)
    │
    ├─► VM 1 (vcc-1): 10.109.0.150
    │   └─► Orchestrator Service (Flask) - Port 5001
    │       • Accepts POST /book-hotel requests (no body required)
    │       • Coordinates with Availability and Payment services
    │       • Returns consolidated booking confirmations
    │
    ├─► VM 2 (vcc-2): 10.109.0.151
    │   └─► Availability Service (Flask) - Port 5002
    │       • Checks room availability and pricing
    │       • Maintains mock hotel database
    │       • Returns availability details
    │
    └─► VM 3 (vcc-3): 10.109.0.152
        └─► Payment Service (Flask) - Port 5003
            • Processes payment transactions
            • Validates payment methods
            • Returns payment confirmations
```

### Service Communication Flow

```
Client (HTTP POST /book-hotel)
    ↓
Orchestrator Service (10.109.0.150:5001)
    ├─ No request body required (hardcoded booking: Lakshya Vashisth at Grand Plaza, Suite)
    ├─ POST /book-hotel (Main orchestration endpoint)
    └─ Calls Availability Service
        ↓
        HTTP POST to Availability at 10.109.0.151:5002
        ↓
Availability Service (10.109.0.151:5002)
    ├─ GET / (Welcome)
    ├─ POST /check-availability (Check room availability)
    └─ GET /hotels (List available hotels)
        ↓
        HTTP Response with room details
        ↓
Orchestrator then calls Payment Service (if available)
    ↓
    HTTP POST to Payment at 10.109.0.152:5003
    ↓
Payment Service (10.109.0.152:5003)
    ├─ GET / (Welcome)
    ├─ POST /process-payment (Process payment)
    └─ GET /payment-status/<txn_id> (Check payment status)
        ↓
        HTTP Response with payment confirmation
        ↓
Returns consolidated booking confirmation to Client
```

---

## 🚀 Quick Start

### Prerequisites
- VirtualBox 7.0+ installed
- Host machine with 8GB+ RAM
- 50GB+ free disk space
- Python 3.9+ on host (for testing)
- curl or Postman for API testing

### Basic Setup (30-45 minutes)

#### 1. **Create and Configure VMs**

Follow the detailed instructions in [VIRTUALBOX_SETUP_GUIDE.md](VIRTUALBOX_SETUP_GUIDE.md):
- Create three Ubuntu 22.04 LTS VMs
- Configure host-only network
- Assign static IPs (10.109.0.150, 10.109.0.151, 10.109.0.152)

#### 2. **Deploy Services**

On VM 1 (vcc-1) - Orchestrator:
```bash
cd ~/microservices/vcc-1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

On VM 2 (vcc-2) - Availability:
```bash
cd ~/microservices/vcc-2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

On VM 3 (vcc-3) - Payment:
```bash
cd ~/microservices/vcc-3
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

#### 3. **Test Communication**

```bash
# Test Orchestrator
curl http://10.109.0.150:5001/

# Test Availability
curl http://10.109.0.151:5002/

# Test Payment
curl http://10.109.0.152:5003/

# Test complete booking flow (no body required)
curl -X POST http://10.109.0.150:5001/book-hotel
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [VIRTUALBOX_SETUP_GUIDE.md](VIRTUALBOX_SETUP_GUIDE.md) | Complete VirtualBox setup, VM creation, and network configuration |
| [ARCHITECTURE_DESIGN.md](ARCHITECTURE_DESIGN.md) | System architecture, diagrams, and design documentation |
| [DEPLOYMENT_INSTRUCTIONS.md](DEPLOYMENT_INSTRUCTIONS.md) | Step-by-step deployment and testing procedures |
| [PLAGIARISM_CLAUSE.md](PLAGIARISM_CLAUSE.md) | Academic integrity and plagiarism policy |

---

## 📁 Directory Structure

```
vcc-1/
├── app.py                    # Orchestrator microservice
├── requirements.txt          # Python dependencies
└── venv/                     # Virtual environment (created during setup)

vcc-2/
├── app.py                    # Availability microservice
├── requirements.txt          # Python dependencies
└── venv/                     # Virtual environment (created during setup)

vcc-3/
├── app.py                    # Payment microservice
├── requirements.txt          # Python dependencies
└── venv/                     # Virtual environment (created during setup)

VIRTUALBOX_SETUP_GUIDE.md     # VM and network setup documentation
ARCHITECTURE_DESIGN.md        # Architecture and design diagrams
DEPLOYMENT_INSTRUCTIONS.md    # Deployment procedures
PLAGIARISM_CLAUSE.md         # Academic integrity statement
README.md                     # This file
```

---

## 🔧 Technologies Used

### Microservices
- **Framework:** Flask 3.1.2
- **Language:** Python 3.9+
- **HTTP Client:** requests library 2.32.5

### Infrastructure
- **Virtualization:** VirtualBox 7.0+
- **Operating System:** Ubuntu 22.04 LTS
- **Networking:** Host-only network adapter
- **Network Protocol:** IPv4

### Tools & Utilities
- **Virtual Environment:** Python venv
- **Package Manager:** pip
- **API Testing:** curl, Postman
- **SSH Client:** OpenSSH

---

## 🔌 API Endpoints

### Orchestrator Service (10.109.0.150:5001)

| Endpoint | Method | Purpose | Request Body | Response |
|----------|--------|---------|--------------|----------|
| `/` | GET | Welcome message | None | Service info and endpoint list |
| `/book-hotel` | POST | Book a hotel (hardcoded) | None (empty/ignored) | Booking confirmation with transaction ID |

**Hardcoded Booking Details:**
- Guest: Lakshya Vashisth
- Hotel: Grand Plaza
- Room: Suite
- Check-in: 2026-02-15
- Check-out: 2026-02-18
- Payment Method: Credit Card

### Availability Service (10.109.0.151:5002)

| Endpoint | Method | Purpose | Request Body | Response |
|----------|--------|---------|--------------|----------|
| `/` | GET | Welcome message | None | Service info and endpoint list |
| `/hotels` | GET | List available hotels | None | List of hotels with room types |
| `/check-availability` | POST | Check room availability | Hotel, dates, room type | Room availability and pricing |

### Payment Service (10.109.0.152:5003)

| Endpoint | Method | Purpose | Request Body | Response |
|----------|--------|---------|--------------|----------|
| `/` | GET | Welcome message | None | Service info and endpoint list |
| `/process-payment` | POST | Process payment | Booking and payment details | Payment confirmation |
| `/payment-status/<txn_id>` | GET | Check payment status | None (in URL) | Payment transaction details |

---

## ✅ Testing Checklist

- [ ] VMs created and running
- [ ] Network connectivity verified (`ping` tests)
- [ ] Static IPs assigned correctly (10.109.0.150, 10.109.0.151, 10.109.0.152)
- [ ] Orchestrator running on port 5001
- [ ] Availability running on port 5002
- [ ] Payment running on port 5003
- [ ] Orchestrator `/` endpoint responds
- [ ] Availability `/hotels` endpoint responds
- [ ] Payment `/` endpoint responds
- [ ] POST to Orchestrator `/book-hotel` (no body) returns booking confirmation
- [ ] Transaction ID included in booking response
- [ ] Complete end-to-end booking workflow working
- [ ] Service names properly reflected in output (Orchestrator, Availability, Payment)

---

## 🐛 Troubleshooting

### Common Issues

**VMs cannot communicate:**
- Verify network adapter is "Host-only"
- Check static IPs are correctly assigned
- Ensure firewall allows ports 5001 and 5002
- Test with `ping` command

**Ports already in use:**
```bash
lsof -i :5001  # Find process using port
kill -9 <PID>   # Kill the process
```

**Python modules not found:**
```bash
source venv/bin/activate           # Activate virtual environment
pip install -r requirements.txt    # Reinstall dependencies
```

For detailed troubleshooting, see [DEPLOYMENT_INSTRUCTIONS.md](DEPLOYMENT_INSTRUCTIONS.md#troubleshooting-deployment).

---

## 📝 Notes

### Hardcoded IP Addresses

The microservices use hardcoded IP addresses for educational purposes:
- Orchestrator: 10.109.0.150
- Availability: 10.109.0.151
- Payment: 10.109.0.152

**For production environments:**
- Use environment variables or configuration files
- Implement service discovery (Consul, Eureka)
- Use container orchestration (Kubernetes)
- Implement proper configuration management

### Service Responses

All service responses are cleaned and role-focused:
- No service identifier fields in responses
- Responses contain only business-relevant data
- Error messages remain descriptive
- Timestamp information included where appropriate

### Debug Mode

Flask applications run with `debug=True` (development mode). **Never use in production.**

### Educational Purpose

This project is designed for learning and demonstration. It is not suitable for production use without significant modifications including security enhancements, error handling, and performance optimizations.

---

## 🔒 Academic Integrity

**See [PLAGIARISM_CLAUSE.md](PLAGIARISM_CLAUSE.md) for the complete academic integrity policy and plagiarism statement.**

---

## 📞 Support & Questions

For issues or questions:
1. Check the relevant documentation file (see [Documentation](#-documentation) section)
2. Review [DEPLOYMENT_INSTRUCTIONS.md](DEPLOYMENT_INSTRUCTIONS.md#troubleshooting-deployment) troubleshooting section
3. Verify network connectivity and VM status
4. Check application logs in Flask output

---

## 📊 Project Specifications

| Aspect | Specification |
|--------|---------------|
| **VM Count** | 3 VMs |
| **Hypervisor** | VirtualBox |
| **Network Type** | Host-only (internal) |
| **Service Type** | Flask microservices |
| **Communication** | HTTP REST API |
| **IP Range** | 10.109.0.0/23 |
| **Orchestrator Port** | 5001 |
| **Availability Port** | 5002 |
| **Payment Port** | 5003 |
| **Python Version** | 3.9+ |
| **Framework Version** | Flask 3.1.2 |

---

## 📄 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Feb 1, 2026 | Initial release with dual microservices |

---

## 📜 License

This project is created for educational purposes. Use, modify, and distribute freely for learning purposes.

---

## ✨ Summary

This project successfully demonstrates:
- ✅ Multi-VM environment setup using VirtualBox (3 VMs)
- ✅ Network configuration and static IP assignment
- ✅ Flask microservices deployment with role-based naming
- ✅ Service orchestration with hardcoded values
- ✅ Inter-service communication with simplified responses
- ✅ Hotel booking workflow end-to-end
- ✅ Comprehensive documentation
- ✅ Complete API testing procedures

All deliverables have been created and are ready for implementation and testing.

**For implementation details, start with [VIRTUALBOX_SETUP_GUIDE.md](VIRTUALBOX_SETUP_GUIDE.md)**

---

**Last Updated:** February 1, 2026  
**Project Status:** ✅ Complete and Ready for Implementation
