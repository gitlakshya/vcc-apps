#!/usr/bin/env bash
set -euo pipefail

# -----------------------------
# Project Configuration
# -----------------------------
PROJECT="vcc-assignment-488811"
REGION="asia-south1"
ZONE="asia-south1-a"
NETWORK="default"

# -----------------------------
# Compute Settings
# -----------------------------
TEMPLATE="vcc-assignment-temp"
GROUP="vcc-assign"
INSTANCE_TYPE="e2-micro"
IMAGE_FAMILY="debian-12"
IMAGE_PROJECT="debian-cloud"
NETWORK_LABEL="vcc-2"

MIN_REPLICAS=1
MAX_REPLICAS=4
CPU_THRESHOLD=0.60
COOLDOWN=60s

# -----------------------------
# IAM Configuration
# -----------------------------
SERVICE_ACCOUNT="vcc-sa"
SERVICE_EMAIL="${SERVICE_ACCOUNT}@${PROJECT}.iam.gserviceaccount.com"
ROLE="roles/compute.viewer"

# -----------------------------
# Firewall Configuration
# -----------------------------
RULE_DENY="deny-all-ingress"
RULE_HTTP="allow-http"
RULE_HTTPS="allow-https"
RULE_SSH="allow-ssh-restricted"
ADMIN_RANGE="103.216.71.79"

# -----------------------------
# Set Project Context
# -----------------------------
gcloud config set project "$PROJECT"
gcloud config set compute/zone "$ZONE"
gcloud config set compute/region "$REGION"

# -----------------------------
# 1. Create Service Account
# -----------------------------
if ! gcloud iam service-accounts describe "$SERVICE_EMAIL" &>/dev/null; then
  gcloud iam service-accounts create "$SERVICE_ACCOUNT" \
    --display-name="Web Tier Service Account"
fi

gcloud projects add-iam-policy-binding "$PROJECT" \
  --member="serviceAccount:${SERVICE_EMAIL}" \
  --role="$ROLE" \
  --condition=None

# -----------------------------
# 2. Configure Firewall Rules
# -----------------------------
gcloud compute firewall-rules create "$RULE_DENY" \
  --network="$NETWORK" \
  --direction=INGRESS \
  --action=DENY \
  --rules=all \
  --priority=65534 2>/dev/null || true

gcloud compute firewall-rules create "$RULE_HTTP" \
  --network="$NETWORK" \
  --direction=INGRESS \
  --action=ALLOW \
  --rules=tcp:80 \
  --target-tags="$NETWORK_LABEL" 2>/dev/null || true

gcloud compute firewall-rules create "$RULE_HTTPS" \
  --network="$NETWORK" \
  --direction=INGRESS \
  --action=ALLOW \
  --rules=tcp:443 \
  --target-tags="$NETWORK_LABEL" 2>/dev/null || true

gcloud compute firewall-rules create "$RULE_SSH" \
  --network="$NETWORK" \
  --direction=INGRESS \
  --action=ALLOW \
  --rules=tcp:22 \
  --source-ranges="$ADMIN_RANGE" \
  --target-tags="$NETWORK_LABEL" 2>/dev/null || true

# -----------------------------
# 3. Create Instance Template
# -----------------------------
gcloud compute instance-templates create "$TEMPLATE" \
  --machine-type="$INSTANCE_TYPE" \
  --image-family="$IMAGE_FAMILY" \
  --image-project="$IMAGE_PROJECT" \
  --tags="$NETWORK_LABEL" \
  --service-account="$SERVICE_EMAIL" \
  --metadata=startup-script='#!/bin/bash
apt update -y
apt install -y apache2
systemctl enable apache2
systemctl start apache2
echo "<h1>Server $(hostname) is active</h1>" > /var/www/html/index.html' \
  2>/dev/null || true

# -----------------------------
# 4. Create Managed Instance Group
# -----------------------------
gcloud compute instance-groups managed create "$GROUP" \
  --template="$TEMPLATE" \
  --size="$MIN_REPLICAS" \
  --zone="$ZONE" 2>/dev/null || true

# -----------------------------
# 5. Attach Autoscaler
# -----------------------------
gcloud compute instance-groups managed set-autoscaling "$GROUP" \
  --zone="$ZONE" \
  --min-num-replicas="$MIN_REPLICAS" \
  --max-num-replicas="$MAX_REPLICAS" \
  --target-cpu-utilization="$CPU_THRESHOLD" \
  --cool-down-period="$COOLDOWN"

echo "Deployment completed successfully."