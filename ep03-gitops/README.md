# EP03 -- GitOps on Kubernetes (ArgoCD)

Deploy and manage Kubernetes workloads declaratively using ArgoCD and Git as the single source of truth.

:tv: Watch the full episode: https://www.youtube.com/watch?v=S6KqZcNNIpY

## Prerequisites

- A running k3d cluster (or any Kubernetes cluster)
- [Helm](https://helm.sh/) installed
- [ArgoCD CLI](https://argo-cd.readthedocs.io/en/stable/cli_installation/) (optional, for CLI commands)

## Quickstart

```bash
# 1. Create a local cluster
k3d cluster create gitops --servers 1

# 2. Install ArgoCD via Helm
helm repo add argo https://argoproj.github.io/argo-helm && helm repo update
helm install argocd argo/argo-cd -n argocd --create-namespace \
  --set server.service.type=ClusterIP \
  --set configs.params."server.insecure"=true --wait

# 3. Get the initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d; echo

# 4. Port-forward the ArgoCD UI (open http://localhost:8080)
kubectl port-forward svc/argocd-server 8080:80 -n argocd &

# 5. Deploy the storefront app via ArgoCD
kubectl apply -f argocd-app.yaml

# 6. Watch ArgoCD sync the application
argocd app get storefront
```

## The GitOps Loop

Once the app is synced, make a change in Git and watch ArgoCD automatically deploy it:

```bash
# Edit storefront.yaml, e.g. change replicas: 1 -> replicas: 3
git add . && git commit -m "scale frontend to 3 replicas" && git push
# ArgoCD detects the new commit and scales automatically!
```

## Self-Healing Demo

Try manually scaling and watch ArgoCD revert it:

```bash
kubectl scale deployment frontend -n shop --replicas=1
# Wait ~30 seconds, then check:
kubectl get pods -n shop -l app=frontend
# ArgoCD self-heals back to 3 replicas!
```
