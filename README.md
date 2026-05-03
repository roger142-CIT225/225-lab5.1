# 225-lab5.1 — CIT225 Final CI/CD Pipeline

![Build Status](http://10.48.229.161:8080/buildStatus/icon?job=roger142-225-lab5.1)

## Pipeline Stages
- Checkout
- Lint HTML
- Build Docker Image
- Push Docker Image
- Deploy to Dev
- Health Check
- Acceptance Tests
- DAST Security Scan
- Deploy to Prod
- Check Kubernetes Cluster

## Environments
- **DEV:** http://10.48.229.161:32000
- **PROD:** http://10.48.228.117
