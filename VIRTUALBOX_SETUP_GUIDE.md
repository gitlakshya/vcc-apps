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

This guide provides comprehensive instructions for setting up a multi-VM microservices environment using VirtualBox. The project demonstrates inter-service communication between two Flask-based microservices deployed on separate virtual machines.

**Educational Purpose:** This project is created for educational purposes to understand microservices architecture, VM management, and network configuration.

---

## Architecture Overview

The system consists of:
- **VM 1 (vcc-1):** Hosts Service A - Communicates with Service B
  - IP Address: `192.168.1.10`
  - Port: `5001`
  
- **VM 2 (vcc-2):** Hosts Service B - Responds to Service A
  - IP Address: `192.168.1.11`
  - Port: `5002`

Communication flow:
```
Service A (192.168.1.10:5001) 
    ↓
Makes HTTP Request to Service B
    ↓
Service B (192.168.1.11:5002) 
    ↓
Returns Hardcoded Response
```

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

### VM 1 (Service A - VCC-1)

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

### VM 2 (Service B - VCC-2)

Repeat the same steps with:
- **Name:** `vcc-2`
- **Hostname:** `vcc-2`
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

#### VM 1 (vcc-1) - IP: 192.168.1.10

SSH into VM and edit network configuration:

```bash
# For Ubuntu 22.04 (Netplan)
sudo nano /etc/netplan/01-netcfg.yaml
```

Add the following configuration:
```yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: no
      addresses:
        - 192.168.1.10/24
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```

Apply the configuration:
```bash
sudo netplan apply
```

Verify:
```bash
ip addr show
# Should show 192.168.1.10
```

#### VM 2 (vcc-2) - IP: 192.168.1.11

Repeat the same process with IP address `192.168.1.11`

```yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: no
      addresses:
        - 192.168.1.11/24
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```

### Step 3: Test Network Connectivity

From VM 1, ping VM 2:
```bash
ping 192.168.1.11
# Expected: Should receive response
```

From VM 2, ping VM 1:
```bash
ping 192.168.1.10
# Expected: Should receive response
```

---

## Microservice Deployment

### On VM 1 (Service A - vcc-1):

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
Edit `app.py` and confirm:
- `SERVICE_B_IP = "192.168.1.11"`
- `SERVICE_B_PORT = 5002`

#### Step 5: Run Service A
```bash
python app.py

# Expected output:
# Starting Service-A-VCC-1...
# Service A will run on port 5001
# Running on http://0.0.0.0:5001
```

### On VM 2 (Service B - vcc-2):

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
# Starting Service-B-VCC-2...
# Service B will run on port 5002
# Running on http://0.0.0.0:5002
```

---

## Testing Inter-Service Communication

### Test 1: Check Health of Service A
From any machine on the network:
```bash
curl http://192.168.1.10:5001/health

# Expected response:
# {
#   "status": "healthy",
#   "service": "Service-A-VCC-1",
#   "message": "Service A is running"
# }
```

### Test 2: Check Health of Service B
```bash
curl http://192.168.1.11:5002/health

# Expected response:
# {
#   "status": "healthy",
#   "service": "Service-B-VCC-2",
#   "message": "Service B is running"
# }
```

### Test 3: Service A Calling Service B
```bash
curl http://192.168.1.10:5001/call-service-b

# Expected response:
# {
#   "caller": "Service-A-VCC-1",
#   "caller_port": 5001,
#   "message": "Successfully called Service B",
#   "service_b_response": {
#     "service_name": "Service-B-VCC-2",
#     "port": 5002,
#     "message": "This is a hardcoded response from Service B",
#     "data": {
#       "status": "success",
#       "timestamp": "2026-02-01",
#       "purpose": "Educational - Inter-service communication demonstration"
#     }
#   }
# }
```

### Test 4: Service Information
```bash
# Get Service A info
curl http://192.168.1.10:5001/info

# Get Service B info
curl http://192.168.1.11:5002/info
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
ping 192.168.1.1  # ping gateway
```

**Solution 2:** Check Firewall
```bash
# On Ubuntu, temporarily disable firewall
sudo ufw disable

# Or allow ports
sudo ufw allow 5001
sudo ufw allow 5002
```

**Solution 3:** Verify VirtualBox Network Settings
- Go to VM Settings → Network
- Ensure both VMs are on the same "Host-only Adapter"
- Network mask should be identical (255.255.255.0)

### Issue: Service B Not Responding

**Solution 1:** Verify Service B is Running
```bash
# On VM 2
netstat -an | grep 5002
# Should show LISTEN on port 5002
```

**Solution 2:** Check Service B Logs
```bash
# Look for error messages in the Flask output
# Common issues: Port already in use, binding to wrong interface
```

**Solution 3:** Test Local Connectivity
```bash
# On VM 2
curl http://localhost:5002/health
# If this works but remote doesn't, firewall issue is likely
```

### Issue: Port Already in Use

```bash
# Find process using port 5001
lsof -i :5001

# Kill the process
kill -9 <PID>
```

### Issue: Python Package Installation Fails

```bash
# Upgrade pip
python3 -m pip install --upgrade pip

# Install with specific version constraints
pip install Flask==3.1.2 requests==2.32.5

# Check installation
pip list | grep -i flask
```

---

## Additional Commands

### SSH into VM from Host

```bash
# From host machine (if SSH is enabled)
ssh vcc@192.168.1.10
ssh vcc@192.168.1.11
```

### Start VMs in Headless Mode
```bash
VBoxManage startvm vcc-1 --type headless
VBoxManage startvm vcc-2 --type headless
```

### Stop VMs Gracefully
```bash
VBoxManage controlvm vcc-1 poweroff
VBoxManage controlvm vcc-2 poweroff
```

### View VM Information
```bash
VBoxManage list vms
VBoxManage showvminfo vcc-1
```

---

## Summary

This guide provides a complete setup for a multi-VM microservices environment. The Flask applications deployed are hardcoded to communicate at specific IP addresses (192.168.1.10 and 192.168.1.11) for educational purposes.

For production environments, consider using:
- Service discovery systems (Consul, Eureka)
- Container orchestration (Kubernetes, Docker Swarm)
- Configuration management tools (Ansible, Terraform)
- Load balancing solutions

---

**Last Updated:** February 1, 2026
