# EP02 — Autoscaling on Kubernetes (HPA & Traffic Surges)

Learn how to configure Horizontal Pod Autoscaler (HPA) to scale your workloads automatically under load surges.

📺 Watch the full episode: https://youtu.be/6z7CbYLzOn4

## Quickstart

```bash
# 1. Create a local cluster (metrics-server is included in k3s)
k3d cluster create autoscaling --servers 1

# 2. Deploy the CPU-intensive workload (includes CPU requests)
kubectl apply -f deployment.yaml

# 3. Apply the HPA manifest (min 2, max 10, target 50% CPU)
kubectl apply -f hpa.yaml

# 4. Watch HPA in real-time
kubectl get hpa php-apache -w

# 5. In a second terminal, trigger the load generator
kubectl apply -f loadgen.yaml
```

Observe your deployment scale from 2 replicas up to 10 as CPU utilization spikes past the 50% target!
