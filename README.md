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
- ✅ `vcc-1/app.py` - Service A microservice code
- ✅ `vcc-1/requirements.txt` - Dependencies for Service A
- ✅ `vcc-2/app.py` - Service B microservice code
- ✅ `vcc-2/requirements.txt` - Dependencies for Service B
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
VirtualBox Host-only Network (vboxnet0: 192.168.1.0/24)
    │
    ├─► VM 1 (vcc-1): 192.168.1.10
    │   └─► Service A (Flask) - Port 5001
    │       • Initiates communication with Service B
    │       • Calls /response endpoint on Service B
    │       • Returns hardcoded responses
    │
    └─► VM 2 (vcc-2): 192.168.1.11
        └─► Service B (Flask) - Port 5002
            • Listens for requests from Service A
            • Responds with hardcoded data
            • Health check available
```

### Service Communication Flow

```
Client (HTTP Request)
    ↓
Service A (192.168.1.10:5001)
    ├─ GET / (Welcome)
    ├─ GET /health (Health check)
    ├─ GET /info (Service information)
    └─ GET /call-service-b (Calls Service B at 192.168.1.11:5002)
        ↓
        HTTP Request to Service B
        ↓
Service B (192.168.1.11:5002)
    ├─ GET / (Welcome)
    ├─ GET /health (Health check)
    ├─ GET /info (Service information)
    └─ GET /response (Returns hardcoded response)
        ↓
        HTTP Response
        ↓
Service A wraps response
    ↓
Returns to Client
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
- Create two Ubuntu 22.04 LTS VMs
- Configure host-only network
- Assign static IPs (192.168.1.10 and 192.168.1.11)

#### 2. **Deploy Services**

On VM 1 (vcc-1):
```bash
cd ~/microservices/vcc-1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

On VM 2 (vcc-2):
```bash
cd ~/microservices/vcc-2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

#### 3. **Test Communication**

```bash
# Test Service A
curl http://192.168.1.10:5001/health

# Test Service B
curl http://192.168.1.11:5002/health

# Test inter-service communication
curl http://192.168.1.10:5001/call-service-b
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
├── app.py                    # Service A microservice
├── requirements.txt          # Python dependencies
└── venv/                     # Virtual environment (created during setup)

vcc-2/
├── app.py                    # Service B microservice
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

### Service A (192.168.1.10:5001)

| Endpoint | Method | Purpose | Response |
|----------|--------|---------|----------|
| `/` | GET | Welcome message | Service info and endpoint list |
| `/health` | GET | Health check | Status: healthy |
| `/info` | GET | Service information | Service name, port, hostname, IP |
| `/call-service-b` | GET | Call Service B | Response from Service B wrapped in Service A response |

### Service B (192.168.1.11:5002)

| Endpoint | Method | Purpose | Response |
|----------|--------|---------|----------|
| `/` | GET | Welcome message | Service info and endpoint list |
| `/health` | GET | Health check | Status: healthy |
| `/info` | GET | Service information | Service name, port, hostname, IP |
| `/response` | GET | Hardcoded response | Hardcoded JSON data from Service B |

---

## ✅ Testing Checklist

- [ ] VMs created and running
- [ ] Network connectivity verified (`ping` tests)
- [ ] Static IPs assigned correctly
- [ ] Service A running on port 5001
- [ ] Service B running on port 5002
- [ ] Service A `/health` endpoint responds
- [ ] Service B `/health` endpoint responds
- [ ] Service A can call Service B via `/call-service-b`
- [ ] Service B returns hardcoded response
- [ ] Complete round-trip communication working

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
- Service A: `SERVICE_B_IP = "192.168.1.11"`
- Service B: Listens on all interfaces (`0.0.0.0`)

**For production environments:**
- Use environment variables or configuration files
- Implement service discovery (Consul, Eureka)
- Use container orchestration (Kubernetes)
- Implement proper configuration management

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
| **VM Count** | 2 VMs |
| **Hypervisor** | VirtualBox |
| **Network Type** | Host-only (internal) |
| **Service Type** | Flask microservices |
| **Communication** | HTTP REST API |
| **IP Range** | 192.168.1.0/24 |
| **Service A Port** | 5001 |
| **Service B Port** | 5002 |
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
- ✅ Multi-VM environment setup using VirtualBox
- ✅ Network configuration and static IP assignment
- ✅ Flask microservices deployment
- ✅ Inter-service communication with hardcoded IPs
- ✅ Comprehensive documentation
- ✅ Complete API testing procedures

All deliverables have been created and are ready for implementation and testing.

**For implementation details, start with [VIRTUALBOX_SETUP_GUIDE.md](VIRTUALBOX_SETUP_GUIDE.md)**

---

**Last Updated:** February 1, 2026  
**Project Status:** ✅ Complete and Ready for Implementation
