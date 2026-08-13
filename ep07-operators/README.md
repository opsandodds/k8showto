# K8s How-To EP7 — Custom Resource Definitions (CRDs) & Kubernetes Operators

Follow-along manifests and commands for **Episode 7: Custom Resource Definitions (CRDs) & Kubernetes Operators** (Series Finale).

## Hands-On Commands

```bash
# 1. Create shop namespace
kubectl create namespace shop

# 2. Register the CustomResourceDefinition (CRD) in the Kubernetes API
kubectl apply -f 01-crd.yaml

# 3. Verify CRD registration in the API server
kubectl get crd databaseclusters.opsandodds.io

# 4. Deploy custom resource instance storefront-db
kubectl apply -f 02-custom-resource.yaml

# 5. Query custom resource using standard kubectl commands & shortnames
kubectl get databaseclusters -n shop
kubectl get dbc storefront-db -n shop -o yaml

# 6. Test OpenAPI v3 schema validation (attempt invalid engine or >10 replicas)
kubectl apply -f - <<EOF
apiVersion: opsandodds.io/v1alpha1
kind: DatabaseCluster
metadata:
  name: invalid-db
  namespace: shop
spec:
  replicas: 99
  engine: oracle
EOF

# 7. Observe operator reconciliation & custom resource status
kubectl get dbc storefront-db -n shop -o jsonpath='{.status}'
```
