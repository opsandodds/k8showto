# K8s How-To EP7 — Custom Resource Definitions (CRDs) & Kubernetes Operators

Follow-along manifests and commands for **Episode 7: Custom Resource Definitions (CRDs) & Kubernetes Operators** (Series Finale).

## Hands-On Commands

```bash
# 1. Verify no existing custom resources
kubectl get crd

# 2. Create target namespace
kubectl create namespace shop

# 3. Register the CustomResourceDefinition (CRD) in the Kubernetes API
kubectl apply -f 01-crd.yaml

# 4. Verify CRD registration in the API server
kubectl get crd databaseclusters.opsandodds.io
kubectl api-resources | grep databasecluster

# 5. Deploy custom resource instance storefront-db
kubectl apply -f 02-custom-resource.yaml

# 6. Query custom resource using standard kubectl commands & shortnames
kubectl get databaseclusters -n shop
kubectl get dbc storefront-db -n shop -o yaml

# 7. Test OpenAPI v3 schema validation (attempt invalid engine or >10 replicas)
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

# 8. Observe operator reconciliation logs
kubectl logs -n kube-system deployment/database-operator --tail=20

# 9. Verify autonomous pod provisioning by the controller
kubectl get pods -n shop -l app.kubernetes.io/managed-by=database-operator

# 10. Scale the custom workload autonomously
kubectl scale dbc storefront-db -n shop --replicas=4
kubectl get pods -n shop -l app.kubernetes.io/managed-by=database-operator

# 11. Graceful Cleanup & Cascading Deletion
kubectl delete dbc storefront-db -n shop
kubectl delete crd databaseclusters.opsandodds.io
```
