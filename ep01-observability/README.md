# EP1 — Observability on Kubernetes (logs, metrics & traces)

Build a complete observability stack on a local Kubernetes cluster — **Prometheus**
(metrics), **Loki** (logs), and **Tempo** (traces), all wired into one **Grafana** —
then use it to debug a real microservice bug.

📺 Watch the episode: `https://www.youtube.com/watch?v=VvgfFBpOj68`

The demo app is a tiny storefront: `frontend → checkout → payment`. The **payment**
service fails with a `503` about a third of the time — that's the bug we hunt down.

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [k3d](https://k3d.io/), [kubectl](https://kubernetes.io/docs/tasks/tools/), [helm](https://helm.sh/)

## 1. Create a cluster

```bash
k3d cluster create obs --servers 1
```

## 2. Install the three backends

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
kubectl create namespace observability

helm install loki       grafana/loki       -n observability -f loki-values.yaml
helm install tempo       grafana/tempo      -n observability
helm install prometheus  prometheus-community/prometheus -n observability \
  --set alertmanager.enabled=false --set server.persistentVolume.enabled=false
```

## 3. Install Grafana (datasources pre-wired) + the log agent

```bash
helm install grafana  grafana/grafana  -n observability -f grafana-values.yaml
helm install promtail grafana/promtail -n observability \
  --set 'config.clients[0].url=http://loki:3100/loki/api/v1/push'

# wait until everything is Running
kubectl get pods -n observability
```

## 4. Build & deploy the demo storefront

```bash
# build the OpenTelemetry-instrumented app image and load it into k3d
docker build -t storefront-demo:1 ./demo
k3d image import storefront-demo:1 -c obs

kubectl apply -f demo/storefront.yaml
kubectl get pods -n shop
```

## 5. Open Grafana

```bash
kubectl port-forward svc/grafana 3000:80 -n observability
# open http://localhost:3000  (user: admin  ·  password: admin — CHANGE THIS for anything real)
```

Go to **Explore** and try each signal:

| Signal  | Datasource | Query |
|---------|------------|-------|
| Metrics | Prometheus | `sum by (mode) (rate(node_cpu_seconds_total[2m]))` |
| Logs    | Loki       | `{namespace="shop", container="app"}` |
| Traces  | Tempo      | Query type **Search** → run, then open a trace to see the `frontend → checkout → payment` waterfall |

**The payoff:** in Explore, hit **Split**, put Loki on one side and Tempo on the
other — the failing logs and the trace of the same request, side by side.

## Clean up

```bash
k3d cluster delete obs
```

---

Part of the **Ops & Odds** K8s How-To series. ⭐ the repo if it helped.
