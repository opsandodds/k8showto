# Episode 5: Secrets Management & Security Hardening (SealedSecrets + Pod SecurityContext)

This folder contains the complete manifests for **Episode 5** of the **Kubernetes How-To** series by **Ops & Odds**.

## Architecture Overview

```
 [ Git Repository ] ──( Safe: Asymmetric RSA Encrypted )──> [ SealedSecret CRD ]
                                                                     │
                                                                     ▼
                                                   [ SealedSecrets Controller ]
                                                                     │ (Decrypts with private key)
                                                                     ▼
 [ Hardened Pod ] <──( Mounted Envs )────────────────── [ K8s Secret (Decrypted) ]
 (runAsNonRoot: true, readOnlyRootFS: true, drop ALL caps)
```

## Quick Start (Follow-Along Guide)

### 1. Create a local k3d cluster
```bash
k3d cluster create demo-cluster
```

### 2. Install SealedSecrets Controller & CLI
```bash
helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
helm install sealed-secrets sealed-secrets/sealed-secrets -n kube-system --wait
```

### 3. Seal your secret with `kubeseal`
```bash
kubectl create namespace shop --dry-run=client -o yaml | kubectl apply -f -
kubeseal --controller-name=sealed-secrets -n kube-system --format yaml < 01-unencrypted-secret.yaml > 02-sealed-secret.yaml
```

### 4. Deploy SealedSecret & Verify Decryption
```bash
kubectl apply -f 02-sealed-secret.yaml
kubectl get sealedsecret db-credentials -n shop
kubectl get secret db-credentials -n shop -o yaml
```

### 5. Deploy Hardened Workload
```bash
kubectl apply -f 03-hardened-deployment.yaml
kubectl get pods -n shop -l app=storefront-web
```

### 6. Verify SecurityContext Compliance
```bash
kubectl exec -it deployment/storefront-web -n shop -- id
# Output: uid=10001(nonroot) gid=10001(nonroot) groups=10001(nonroot)
```
