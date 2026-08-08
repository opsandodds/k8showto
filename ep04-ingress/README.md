# Episode 4: Ingress & TLS Certificates (ingress-nginx + cert-manager)

This folder contains the complete manifests for **Episode 4** of the **Kubernetes How-To** series.

## Architecture Overview

```
[ External User HTTPS ] 
          │
          ▼ (Port 443 / TLS Termination)
 ┌────────────────────────────────────────┐
 │      Ingress Controller (nginx)       │
 └────────────────────────────────────────┘
     │                           │
     ▼ (Path: /)                 ▼ (Path: /api)
 ┌────────────────┐         ┌────────────────┐
 │ storefront-web │         │  api-service   │
 └────────────────┘         └────────────────┘
```

## Quick Start (Follow-Along Guide)

### 1. Create a local k3d cluster with Ingress port mappings
```bash
k3d cluster create demo-cluster -p "80:80@loadbalancer" -p "443:443@loadbalancer"
```

### 2. Install cert-manager
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.14.4/cert-manager.yaml
```

### 3. Deploy ClusterIssuer
```bash
kubectl apply -f cert-manager/cluster-issuer.yaml
```

### 4. Deploy Applications & Ingress Routes
```bash
kubectl apply -f app/storefront.yaml
kubectl apply -f ingress/ingress-routes.yaml
```

### 5. Verify Certificate Issuance
```bash
kubectl get certificate -n shop
kubectl get secret storefront-tls-cert -n shop
```
