# 225-lab5.1 - CIT225 Final CI/CD Pipeline

## Live Environments
- **DEV:** http://10.48.229.161:32000
- **PROD:** http://10.48.228.117

## App Features
- Flask + SQLite contact list (add / delete) with real-time updates (no page reload)
- Live deployment status cards (build, environment, pod name, uptime)
- Modern dark UI with Inter + JetBrains Mono fonts
- Build number, environment (DEV/PROD), and pod name displayed in header badges

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
- Check Kubernetes Cluster (all, ingress, pvc)

## Characteristics Pulled From Each Semester Repo
| Repo | Characteristic |
|---|---|
| 225-lab3-1 | Jenkinsfile, Docker build/push, NodePort 32000 |
| 225-lab3-2 | Slack notifications, Ingress routing |
| 225-lab3-3 | HTML linting |
| 225-lab3-4 | DEV → PROD flow |
| 225-lab3-5 | Pipeline stops on lint failure |
| metallb-deploy | LoadBalancer at 10.48.228.117 |
| 225-lab3-6 | Selenium acceptance tests |
| 225-lab3-7 | DASTardly DAST security scan |
| 225-lab3-8 | Flask app with environment variable injection |
| 225-lab3-9 | SQLite database, persistence demo (data loss on pod delete) |
| 225-lab4-1 | PVC manifest for persistent storage |

## Persistence Demo
1. Open the DEV page and add a contact
2. Open Rancher → Workloads → Pods
3. Find the pod named `dev-deployment-xxxxx` (matches the pod name shown in the page header badge)
4. Click the three dots → Delete
5. Watch the pod name in the badge change as Kubernetes spins up a replacement
6. Refresh the page — the contact is gone
7. Run `kubectl get pvc` — `app-pvc Pending` shows the lab 3-9 problem, `flask-pvc Bound` shows the lab 4-1 fix

## Credentials
- Docker Image: `cithit/roger142`
- Image Tag: `build-${BUILD_NUMBER}`
- GitHub: `https://github.com/roger142-CIT225/225-lab5.1.git`
- Kubeconfig: `roger142-225-sp26`
- DEV IP: `10.48.229.161`
- PROD IP: `10.48.228.117`
