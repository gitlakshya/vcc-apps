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
  - IP Address: `10.109.0.150`
  - Port: `5001`
  
- **VM 2 (vcc-2):** Hosts Service B - Responds to Service A and calls back to Service A
  - IP Address: `10.109.0.151`
  - Port: `5002`

Communication flow:
```
Service A (10.109.0.150:5001) 
    ↓
Makes HTTP Request to Service B
    ↓
Service B (10.109.0.151:5002) 
    ↓
Returns Response
    ↓
Service B also calls back to Service A (bidirectional)
    ↓
Service A (10.109.0.150:5001)
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
   - **Memory:** 2048 MhB minimum (4096 MB recommended)
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
- `SERVICE_B_IP = "10.109.0.151"`
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
curl http://10.109.0.150:5001/health

# Expected response:
# {
#   "status": "healthy",
#   "service": "Service-A-VCC-1",
#   "message": "Service A is running"
# }
```

### Test 2: Check Health of Service B
```bash
curl http://10.109.0.151:5002/health

# Expected response:
# {
#   "status": "healthy",
#   "service": "Service-B-VCC-2",
#   "message": "Service B is running"
# }
```

### Test 3: Service A Calling Service B
```bash
curl http://10.109.0.150:5001/call-service-b

# Expected response:
# {
#   "caller": "Service-A-VCC-1",
#   "caller_port": 5001,
#   "message": "Successfully called Service B",
#   "service_b_response": { ... }
# }
```

### Test 4: Service B Calling Service A (Bidirectional Communication)
```bash
curl http://10.109.0.151:5002/call-service-a

# Expected response:
# {
#   "caller": "Service-B-VCC-2",
#   "caller_port": 5002,
#   "message": "Successfully called Service A",
#   "service_a_response": { ... }
# }
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
# Ensure you're in the virtual environment
source venv/bin/activate

# Upgrade pip inside venv
python -m pip install --upgrade pip

# Install with specific version constraints (NO --user flag in venv!)
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

# 3. Use whichever file exists. For 50-cloud-init.yaml:
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
