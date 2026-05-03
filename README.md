# 225-lab5.1 — CIT225 Final CI/CD Pipeline

## Live Environments
- **DEV:** http://10.48.229.161:32000
- **PROD:** http://10.48.228.117

## Pipeline Stages
- Cleanup Old Services
- Checkout
- Lint HTML
- Build Docker Image
- Push Docker Image
- Deploy to Dev (Deployment + Ingress + PVC)
- Health Check (curl)
- Acceptance Tests (Selenium)
- DAST Security Scan (DASTardly)
- Deploy to Prod
- Check Kubernetes Cluster

## App Features
- Flask + SQLite contact list (add / delete)
- Live build number displayed on the page
- Demonstrates persistence behavior from lab 3-9 vs lab 4-1

## Characteristics Pulled From Each Semester Repo
| Repo | Characteristic |
|---|---|
| 225-lab3-1 | Jenkinsfile, Docker build/push, NodePort 32000 |
| 225-lab3-2 | Slack notifications, Ingress |
| 225-lab3-3 | HTML linting |
| 225-lab3-4 | DEV → PROD flow |
| 225-lab3-5 | Pipeline stops on lint failure |
| metallb-deploy | LoadBalancer at 10.48.228.117 |
| 225-lab3-6 | Selenium acceptance tests |
| 225-lab3-7 | DASTardly DAST security scan |
| 225-lab3-8 | Deployment manifests with
