# VirtualBox VM Setup and Microservices Deployment Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [Prerequisites](#prerequisites)
4. [Step-by-Step VirtualBox Installation](#step-by-step-virtualbox-installation)
5. [Creating Virtual Machines](#creating-virtual-machines)
6. [Network Configuration](#network-configuration)
7. [Microservice Deployment](#microservice-deployment)
8. [Testing Inter-Service Communication](#testing-inter-service-communication)
9. [Troubleshooting](#troubleshooting)

---

## Introduction

This guide provides comprehensive instructions for setting up a multi-VM microservices environment using VirtualBox. The project demonstrates a **hotel booking system** built on three Flask-based microservices deployed on separate virtual machines. The system showcases service orchestration, inter-service communication, and practical microservices architecture patterns.

**Educational Purpose:** This project is created for educational purposes to understand microservices architecture, service orchestration, VM management, and network configuration.

---

## Architecture Overview

The system consists of a **three-tier microservices hotel booking application**:

- **VM 1 (vcc-1):** Booking Orchestrator Service - Coordinates hotel bookings
  - IP Address: `10.109.0.150`
  - Port: `5001`
  - Hardcoded Booking: Lakshya Vashisth at Grand Plaza, Suite (2026-02-15 to 2026-02-18)
  
- **VM 2 (vcc-2):** Room Availability Service - Checks room availability and pricing
  - IP Address: `10.109.0.151`
  - Port: `5002`
  - Maintains mock hotel database

- **VM 3 (vcc-3):** Payment Processing Service - Processes booking payments
  - IP Address: `10.109.0.152`
  - Port: `5003`
  - Validates payment methods

### Hotel Booking Workflow

```
Client Request (POST /book-hotel to Orchestrator)
    ├─ No request body required (uses hardcoded values)
    ↓
Orchestrator receives request and initiates workflow
    ↓
Step 1: Orchestrator calls Availability Service (10.109.0.151:5002)
    ├─ Checks: Grand Plaza, Suite, 2026-02-15 to 2026-02-18
    ↓
Availability Service returns room details (rate, availability, nights)
    ↓
Step 2: If available → Orchestrator calls Payment Service (10.109.0.152:5003)
    ├─ Amount = room_rate × num_nights
    ├─ Payment Method = credit_card (hardcoded)
    ↓
Payment Service processes payment (95% success rate)
    ↓
Step 3: If payment approved → Orchestrator returns consolidated booking confirmation
    ├─ Booking ID, Transaction ID, pricing breakdown
    ├─ No service identifier fields in response
    ↓
If any step fails → Orchestrator returns error with details
```

### Hardcoded Hotel Database

Service B maintains a mock hotel database with sample hotels:

| Hotel Name | City | Room Types | Status |
|---|---|---|---|
| Grand Plaza | New York | Standard, Deluxe, Suite | Available |
| Oceanview Resort | Miami | Standard, Deluxe, Suite | Available |
| City Center Inn | Chicago | Standard, Deluxe, Suite | Available |

Each room type has predefined daily rates and availability counts.

---

## Prerequisites

### Host Machine Requirements:
- **VirtualBox:** Version 7.0 or higher
- **RAM:** Minimum 8GB (2GB per VM recommended)
- **Storage:** Minimum 50GB free space
- **Linux/Windows/macOS** with virtualization enabled

### Network Requirements:
- Bridge network adapter available on host
- Static IP assignment capability

---

## Step-by-Step VirtualBox Installation

### On macOS:
```bash
# Using Homebrew
brew install --cask virtualbox

# Verify installation
VirtualBox --version
```

### On Windows:
1. Download from: https://www.virtualbox.org/wiki/Downloads
2. Run the installer executable
3. Follow the installation wizard
4. Restart the computer when prompted

### On Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install virtualbox

# Verify installation
virtualbox --version
```

---

## Creating Virtual Machines

### VM 1 (Booking Orchestrator - VCC-1)

#### Step 1: Create VM
1. Open VirtualBox
2. Click "New"
3. Configure:
   - **Name:** `vcc-1`
   - **Machine Folder:** Default or custom location
   - **Type:** Linux or appropriate OS
   - **Version:** Ubuntu 22.04 LTS (recommended)
   - **Memory:** 2048 MB minimum (4096 MB recommended)
   - **Storage:** 20GB dynamic allocation

#### Step 2: Install Operating System
1. Download Ubuntu 22.04 LTS ISO from https://ubuntu.com/download/server
2. Select the created VM → Start
3. Select the ISO file when prompted
4. Follow Ubuntu installation wizard
5. Configure:
   - **Hostname:** `vcc-1`
   - **Username:** `vcc` (or your preference)
   - **Packages:** OpenSSH server (for remote access)

#### Step 3: Post-Installation Setup
```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and pip
sudo apt-get install -y python3 python3-pip python3-venv

# Install Git (optional, for cloning source code)
sudo apt-get install -y git

# Install curl (for testing API endpoints)
sudo apt-get install -y curl
```

### VM 2 (Room Availability Service - VCC-2)

Repeat the same steps with:
- **Name:** `vcc-2`
- **Hostname:** `vcc-2`
- Same software packages as VM 1

### VM 3 (Payment Processing Service - VCC-3)

Repeat the same steps with:
- **Name:** `vcc-3`
- **Hostname:** `vcc-3`
- Same software packages as VM 1

---

## Network Configuration

### Step 1: Create Bridge Network (Host-Only or Bridge Mode)

#### Bridged Network (Recommended for inter-VM communication):

**On Host Machine:**

1. Go to VirtualBox → Preferences/Settings → Network
2. Click "Host-only Networks"
3. Create a new network:
   - **Name:** vboxnet0
   - **IPv4 Address:** 192.168.1.1
   - **IPv4 Netmask:** 255.255.255.0
   - **DHCP Server:** Disable or configure range 192.168.1.100-192.168.1.254

**On Each VM:**

1. Select VM → Settings → Network
2. **Adapter 1:**
   - Attached to: "Host-only Adapter"
   - Name: "vboxnet0"
3. Click OK

### Step 2: Configure Static IPs on VMs

#### VM 1 (vcc-1) - IP: 10.109.0.150

SSH into VM 1 and configure static IP using the existing netplan file:

```bash
# Step 1: Check existing netplan files
ls /etc/netplan/
# Should show: 50-cloud-init.yaml (or similar)

# Step 2: Backup the existing file
sudo cp /etc/netplan/50-cloud-init.yaml /etc/netplan/50-cloud-init.yaml.bak

# Step 3: Create new netplan configuration using heredoc (copy-paste friendly)
sudo bash -c 'cat > /etc/netplan/50-cloud-init.yaml << EOF
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s8:
      dhcp4: no
      addresses:
        - 10.109.0.150/23
      routes:
        - to: default
          via: 10.109.0.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
EOF'

# Step 4: Apply the configuration
sudo netplan apply

# Step 5: Verify the configuration
ip addr show enp0s8
# Should show: inet 10.109.0.150/23

ip route show
# Should show default route via 10.109.0.1
```

#### VM 2 (vcc-2) - IP: 10.109.0.151

Repeat the same process on VM 2 with IP address `10.109.0.151`:

```bash
# Step 1: Check existing netplan files
ls /etc/netplan/

# Step 2: Backup the existing file
sudo cp /etc/netplan/50-cloud-init.yaml /etc/netplan/50-cloud-init.yaml.bak

# Step 3: Create new netplan configuration
sudo bash -c 'cat > /etc/netplan/50-cloud-init.yaml << EOF
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s8:
      dhcp4: no
      addresses:
        - 10.109.0.151/23
      routes:
        - to: default
          via: 10.109.0.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
EOF'

# Step 4: Apply the configuration
sudo netplan apply

# Step 5: Verify the configuration
ip addr show enp0s8
# Should show: inet 10.109.0.151/23

ip route show
# Should show default route via 10.109.0.1
```

#### VM 3 (vcc-3) - IP: 10.109.0.152

Repeat the same process on VM 3 with IP address `10.109.0.152`:

```bash
# Step 1: Check existing netplan files
ls /etc/netplan/

# Step 2: Backup the existing file
sudo cp /etc/netplan/50-cloud-init.yaml /etc/netplan/50-cloud-init.yaml.bak

# Step 3: Create new netplan configuration
sudo bash -c 'cat > /etc/netplan/50-cloud-init.yaml << EOF
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s8:
      dhcp4: no
      addresses:
        - 10.109.0.152/23
      routes:
        - to: default
          via: 10.109.0.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
EOF'

# Step 4: Apply the configuration
sudo netplan apply

# Step 5: Verify the configuration
ip addr show enp0s8
# Should show: inet 10.109.0.152/23

ip route show
# Should show default route via 10.109.0.1
```

### Step 3: Test Network Connectivity

From VM 1, ping VM 2 and VM 3:
```bash
ping 10.109.0.151
ping 10.109.0.152
# Expected: Should receive responses
```

From VM 2, ping VM 1 and VM 3:
```bash
ping 10.109.0.150
ping 10.109.0.152
# Expected: Should receive responses
```

From VM 3, ping VM 1 and VM 2:
```bash
ping 10.109.0.150
ping 10.109.0.151
# Expected: Should receive responses
```

---

## Microservice Deployment

### On VM 1 (Booking Orchestrator - vcc-1):

#### Step 1: Copy or Clone Source Code
```bash
# Option 1: Clone from GitHub
git clone <REPOSITORY_URL> /home/vcc/microservices
cd /home/vcc/microservices/vcc-1

# Option 2: Copy files manually
# Transfer app.py and requirements.txt to /home/vcc/vcc-1/
```

#### Step 2: Create and Activate Virtual Environment
```bash
cd /home/vcc/microservices/vcc-1
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Verify Configuration
Edit `app.py` and confirm hardcoded service addresses:
- `SERVICE_B_IP = "10.109.0.151"` (Availability Service)
- `SERVICE_B_PORT = 5002`
- `SERVICE_C_IP = "10.109.0.152"` (Payment Service)
- `SERVICE_C_PORT = 5003`

#### Step 5: Run Service A
```bash
python app.py

# Expected output:
# Starting Service-A-VCC-1 (Hotel Booking Orchestrator)...
# Service: Service-A-VCC-1
# Port: 5001
# Availability Service: 10.109.0.151:5002
# Payment Service: 10.109.0.152:5003
# Running on http://0.0.0.0:5001
```

### On VM 2 (Room Availability Service - vcc-2):

#### Step 1: Copy Source Code
```bash
git clone <REPOSITORY_URL> /home/vcc/microservices
cd /home/vcc/microservices/vcc-2
```

#### Step 2: Create and Activate Virtual Environment
```bash
cd /home/vcc/microservices/vcc-2
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Run Service B
```bash
python app.py

# Expected output:
# Starting Availability Service (Hotel Rooms)...
# Service: Availability
# Port: 5002
# Hotels in database: Grand Plaza, Oceanview Resort, City Center Inn
# Running on http://0.0.0.0:5002
```

### On VM 3 (Payment Processing Service - vcc-3):

#### Step 1: Copy Source Code
```bash
git clone <REPOSITORY_URL> /home/vcc/microservices
cd /home/vcc/microservices/vcc-3
```

#### Step 2: Create and Activate Virtual Environment
```bash
cd /home/vcc/microservices/vcc-3
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Run Payment Service
```bash
python app.py

# Expected output:
# Starting Payment Service (Hotel Booking)...
# Service: Payment
# Port: 5003
# Endpoints: /process-payment, /payment-status/<txn_id>
# Running on http://0.0.0.0:5003
```

---

## Testing Inter-Service Communication

### Test 1: Check Health of All Services

From any machine on the network, verify all services are running:

```bash
## Testing Inter-Service Communication

### Test 1: Welcome Endpoints

From any machine on the network, verify all services are running:

```bash
# Orchestrator
curl http://10.109.0.150:5001/

# Expected response:
# {
#   "port": 5001,
#   "description": "Hotel Booking Orchestrator Service",
#   "endpoints": {
#     "POST /book-hotel": "Book a hotel (orchestrates availability and payment)"
#   }
# }

# Availability
curl http://10.109.0.151:5002/

# Expected response:
# {
#   "port": 5002,
#   "description": "Hotel Room Availability Service",
#   "endpoints": {
#     "POST /check-availability": "Check hotel room availability and pricing",
#     "GET /hotels": "List all available hotels"
#   }
# }

# Payment
curl http://10.109.0.152:5003/

# Expected response:
# {
#   "port": 5003,
#   "description": "Hotel Booking Payment Processing Service",
#   "endpoints": {
#     "POST /process-payment": "Process payment for hotel booking",
#     "GET /payment-status/<transaction_id>": "Check payment status"
#   }
# }
```

### Test 2: Verify Connectivity

Test ping from each VM to confirm network connectivity:

```bash
# From Orchestrator VM
ping 10.109.0.151
ping 10.109.0.152

# From Availability VM
ping 10.109.0.150
ping 10.109.0.152

# From Payment VM
ping 10.109.0.150
ping 10.109.0.151

# All pings should respond with time values (not timeout)
```

### Test 3: List Available Hotels

Check which hotels are available in the system:

```bash
curl http://10.109.0.151:5002/hotels

# Expected response:
# {
#   "status": "success",
#   "available_hotels": [
#     {"name": "Grand Plaza", "city": "New York", "room_types": ["Standard", "Deluxe", "Suite"]},
#     {"name": "Oceanview Resort", "city": "Miami", "room_types": ["Standard", "Deluxe", "Suite"]},
#     {"name": "City Center Inn", "city": "Chicago", "room_types": ["Standard", "Deluxe", "Suite"]}
#   ]
# }
```

### Test 4: Check Room Availability

Query the availability service directly for room availability:

```bash
curl -X POST http://10.109.0.151:5002/check-availability \
  -H "Content-Type: application/json" \
  -d '{
    "hotel_name": "Grand Plaza",
    "check_in": "2026-02-15",
    "check_out": "2026-02-18",
    "room_type": "Suite",
    "num_guests": 1
  }'

# Expected response (room available):
# {
#   "status": "success",
#   "available": true,
#   "hotel_name": "Grand Plaza",
#   "room_type": "Suite",
#   "check_in": "2026-02-15",
#   "check_out": "2026-02-18",
#   "num_nights": 3,
#   "room_rate": 300.00,
#   "total_price": 900.00,
#   "available_rooms": 1,
#   "currency": "USD",
#   "timestamp": "2026-02-01T12:34:56.789123"
# }
```

### Test 5: Complete Hotel Booking Workflow (End-to-End)

This is the main test that demonstrates the full orchestration. The booking requires NO request body - all values are hardcoded:

```bash
curl -X POST http://10.109.0.150:5001/book-hotel

# Expected response (successful booking):
# {
#   "status": "confirmed",
#   "message": "Hotel booking confirmed successfully",
#   "booking_id": "BOOK1738443296",
#   "transaction_id": "TXN1001",
#   "guest_name": "Lakshya Vashisth",
#   "guest_email": "lakshya@example.com",
#   "hotel_name": "Grand Plaza",
#   "room_type": "Suite",
#   "check_in": "2026-02-15",
#   "check_out": "2026-02-18",
#   "number_of_nights": 3,
#   "room_rate_per_night": 300.00,
#   "total_amount": 900.00,
#   "currency": "USD",
#   "payment_status": "approved",
#   "booking_timestamp": "2026-02-01T12:34:56.789123"
# }
```

**Key Differences from Previous Version:**
- No request body required (uses POST /book-hotel with empty body)
- All booking details are hardcoded (Lakshya Vashisth, Grand Plaza, Suite)
- No service identifier fields in the response
- Response focused on booking and payment information only
- Transaction ID included for payment reference

### Test 6: Check Payment Transaction Status

After a successful booking, check the payment transaction:

```bash
curl http://10.109.0.152:5003/payment-status/TXN1001

# Expected response:
# {
#   "status": "success",
#   "transaction_id": "TXN1001",
#   "booking_id": "BOOK1738443296",
#   "guest_name": "Lakshya Vashisth",
#   "hotel_name": "Grand Plaza",
#   "amount": 900.00,
#   "currency": "USD",
#   "payment_status": "approved",
#   "reason": "Payment gateway approval",
#   "timestamp": "2026-02-01T12:34:56.123456"
# }
```

### Test 7: Failed Availability Check

Try to book a room that's not available:

```bash
# First, check which rooms are unavailable
curl -X POST http://10.109.0.151:5002/check-availability \
  -H "Content-Type: application/json" \
  -d '{
    "hotel_name": "City Center Inn",
    "check_in": "2026-02-15",
    "check_out": "2026-02-18",
    "room_type": "Suite",
    "num_guests": 1
  }'

# Expected response (no suites available):
# {
#   "status": "unavailable",
#   "available": false,
#   "hotel_name": "City Center Inn",
#   "room_type": "Suite",
#   "check_in": "2026-02-15",
#   "check_out": "2026-02-18",
#   "message": "No Suite rooms available for the selected dates"
# }
```
```

---

## Troubleshooting

### Issue: VMs Cannot Communicate

**Solution 1:** Verify Network Configuration
```bash
# On each VM, check IP address
ip addr show

# Verify gateway
ip route show

# Test connectivity
ping 10.109.0.1  # ping gateway
```

**Solution 2:** Check Firewall
```bash
# On Ubuntu, temporarily disable firewall
sudo ufw disable

# Or allow specific ports
sudo ufw allow 5001
sudo ufw allow 5002
sudo ufw allow 5003
```

**Solution 3:** Verify VirtualBox Network Settings
- Go to VM Settings → Network
- Ensure all VMs are on the same "Host-only Adapter"
- Network mask should be identical (255.255.255.0)

### Issue: Service Not Responding

**Solution 1:** Verify Service is Running
```bash
# On respective VM, check if service is listening
netstat -an | grep 5001  # For Service A
netstat -an | grep 5002  # For Service B
netstat -an | grep 5003  # For Service C
# Should show LISTEN status
```

**Solution 2:** Check Service Logs
```bash
# Look for error messages in the Flask output
# Common issues: Port already in use, binding to wrong interface, missing dependencies
```

**Solution 3:** Test Local Connectivity
```bash
# On the service VM
curl http://localhost:5001/health  # For Service A
# If this works but remote doesn't, firewall issue is likely
```

### Issue: Hotel Booking Returns Service Unavailable

**Potential Causes:**
- Availability Service (vcc-2) is not running
- Payment Service (vcc-3) is not running
- Network connectivity between VMs is broken
- Service addresses hardcoded in vcc-1/app.py don't match actual IPs

**Solution:**
```bash
# 1. Verify all three services are running
# On vcc-1: curl http://localhost:5001/health
# On vcc-2: curl http://localhost:5002/health
# On vcc-3: curl http://localhost:5003/health

# 2. Check vcc-1 can reach vcc-2 and vcc-3
# On vcc-1:
curl http://10.109.0.151:5002/health  # Should reach vcc-2
curl http://10.109.0.152:5003/health  # Should reach vcc-3

# 3. Verify IP addresses in vcc-1/app.py match actual VM IPs
# On vcc-2: hostname -I (should show 10.109.0.151)
# On vcc-3: hostname -I (should show 10.109.0.152)
```

### Issue: Port Already in Use

```bash
# Find process using port
lsof -i :5001  # For Service A
lsof -i :5002  # For Service B
lsof -i :5003  # For Service C

# Kill the process
kill -9 <PID>

# Or wait for the service to fully shut down before restarting
```

### Issue: Python Package Installation Fails

```bash
# Ensure you're in the virtual environment
source venv/bin/activate

# Upgrade pip inside venv
python -m pip install --upgrade pip

# Install packages (WITHOUT --user flag in venv!)
pip install Flask==3.1.2 requests==2.32.5

# Check installation
pip list | grep -i flask
```

### Issue: "Permission Denied" or "cannot perform a --user install"

**Solution:**
```bash
# 1. Deactivate and exit virtual environment
deactivate

# 2. Remove old venv
rm -rf venv

# 3. Create fresh virtual environment
python3 -m venv venv

# 4. Activate it
source venv/bin/activate

# 5. Verify activation (should see (venv) prefix)
echo $VIRTUAL_ENV

# 6. Upgrade pip
python -m pip install --upgrade pip

# 7. Install packages (WITHOUT --user flag)
pip install Flask==3.1.2 requests==2.32.5
```

### Issue: Netplan Configuration File Not Found

**Solution:**
```bash
# 1. List all netplan files in the directory
ls -la /etc/netplan/

# 2. Common filenames:
#    - 50-cloud-init.yaml (most common on cloud images)
#    - 01-netcfg.yaml (older installations)
#    - 00-installer-config.yaml (new installations)

# 3. Use whichever file exists and apply the IP configuration:
sudo bash -c 'cat > /etc/netplan/50-cloud-init.yaml << EOF
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s8:
      dhcp4: no
      addresses:
        - 10.109.0.150/23
      routes:
        - to: default
          via: 10.109.0.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
EOF'

# 4. Apply configuration
sudo netplan apply
```

### Issue: Service Cannot Process Hotel Booking

**Common Errors:**

1. **"Missing required booking fields"** - Ensure POST request includes all required fields:
   - guest_name, hotel_name, check_in, check_out, room_type, payment_method

2. **"Hotel not found"** - Hotel name must match exactly (case-sensitive). Available hotels:
   - "Grand Plaza"
   - "Oceanview Resort"
   - "City Center Inn"

3. **"Room type not available"** - Verify room type exists for the hotel. Available types:
   - Standard, Deluxe, Suite

4. **"No rooms available"** - Room is sold out. Try different dates or different room type.

5. **"Payment declined"** - Payment amount must be positive. Some amounts >$10,000 are declined by design.

---

## Additional Commands

### SSH into VM from Host

```bash
# From host machine (if SSH is enabled)
ssh vcc@10.109.0.150  # vcc-1 (Booking Orchestrator)
ssh vcc@10.109.0.151  # vcc-2 (Availability Service)
ssh vcc@10.109.0.152  # vcc-3 (Payment Service)
```

### Start VMs in Headless Mode
```bash
VBoxManage startvm vcc-1 --type headless
VBoxManage startvm vcc-2 --type headless
VBoxManage startvm vcc-3 --type headless
```

### Stop VMs Gracefully
```bash
VBoxManage controlvm vcc-1 poweroff
VBoxManage controlvm vcc-2 poweroff
VBoxManage controlvm vcc-3 poweroff
```

### View VM Information
```bash
VBoxManage list vms
VBoxManage showvminfo vcc-1
VBoxManage showvminfo vcc-2
VBoxManage showvminfo vcc-3
```

### Start All Services Together (from host with SSH)

```bash
# Terminal 1: Start Service A (Booking Orchestrator)
ssh vcc@10.109.0.150 'cd /home/vcc/microservices/vcc-1 && source venv/bin/activate && python app.py'

# Terminal 2: Start Service B (Availability Service)
ssh vcc@10.109.0.151 'cd /home/vcc/microservices/vcc-2 && source venv/bin/activate && python app.py'

# Terminal 3: Start Service C (Payment Service)
ssh vcc@10.109.0.152 'cd /home/vcc/microservices/vcc-3 && source venv/bin/activate && python app.py'
```

---

## Summary

This guide provides a complete setup for a **three-tier hotel booking microservices system**. The architecture demonstrates key concepts in distributed systems:

### Key Architecture Patterns Demonstrated:

1. **Service Orchestration** - Service A coordinates workflows across multiple services
2. **Service Composition** - Services call each other to compose business functionality
3. **Fault Isolation** - Failures in one service don't cascade to others
4. **Domain Separation** - Each service manages its own data and logic:
   - Service A: Booking orchestration and validation
   - Service B: Hotel inventory and pricing
   - Service C: Payment processing and transactions
5. **Inter-Service Communication** - HTTP-based REST APIs for synchronous communication
6. **Error Handling** - Proper exception handling and user feedback at each layer

### Services Overview:

| Service | Port | Responsibility | Key Endpoints |
|---------|------|---|---|
| vcc-1 | 5001 | Booking Orchestrator | `/book-hotel`, `/health` |
| vcc-2 | 5002 | Room Availability | `/check-availability`, `/hotels`, `/health` |
| vcc-3 | 5003 | Payment Processing | `/process-payment`, `/payment-status`, `/health` |

### Data Flow:

```
Guest Request
  ↓
Booking Service (vcc-1)
  ├─→ Check Availability Service (vcc-2)
  │   ├─ Verify hotel exists
  │   ├─ Check room availability
  │   └─ Calculate pricing
  ├─→ Payment Service (vcc-3)
  │   ├─ Validate payment method
  │   ├─ Process payment
  │   └─ Generate transaction ID
  └─→ Return Booking Confirmation
      ├─ Booking details
      ├─ Transaction reference
      └─ Services involved
```

### Production Considerations:

For production environments, consider implementing:
- **Service Discovery** - Use Consul, Eureka, or Kubernetes service discovery instead of hardcoded IPs
- **API Gateway** - Route and manage external API calls
- **Load Balancing** - Distribute traffic across multiple service instances
- **Container Orchestration** - Use Kubernetes or Docker Swarm for deployment
- **Configuration Management** - Use environment variables or config servers instead of hardcoded values
- **Monitoring & Logging** - Implement centralized logging and monitoring
- **Message Queues** - Use async messaging for decoupled service communication
- **Circuit Breakers** - Implement resilience patterns for failing services
- **Database Persistence** - Replace in-memory mock data with real databases

### Next Steps:

1. Deploy the services on the VirtualBox VMs
2. Run health checks on all services
3. Test inter-service communication
4. Execute end-to-end hotel booking workflows
5. Experiment with failure scenarios (stop one service, see how others respond)
6. Explore modifying the hardcoded data and business logic

---

**Last Updated:** February 1, 2026
