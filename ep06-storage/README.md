# K8s How-To EP6 — StatefulSets & Storage Classes

Follow-along manifests and commands for **Episode 6: StatefulSets & Storage Classes on Kubernetes**.

## Hands-On Commands

```bash
# 1. Create shop namespace
kubectl create namespace shop

# 2. Apply custom StorageClass with Retain policy
kubectl apply -f 01-storageclass.yaml

# 3. Deploy Headless Service (clusterIP: None)
kubectl apply -f 02-headless-service.yaml

# 4. Deploy StatefulSet with volumeClaimTemplates
kubectl apply -f 03-statefulset.yaml

# 5. Observe ordered pod startup (web-db-0 before web-db-1)
kubectl get pods -n shop -w

# 6. Verify dedicated PV and PVC dynamic allocation
kubectl get pvc,pv -n shop

# 7. Test data persistence across pod deletion
kubectl exec -it web-db-0 -n shop -- sh -c "echo 'hello opsandodds' > /data/persistence_test.txt"
kubectl delete pod web-db-0 -n shop
kubectl exec -it web-db-0 -n shop -- cat /data/persistence_test.txt

# 8. Test Headless Service DNS resolution between pods
kubectl exec -it web-db-1 -n shop -- nslookup web-db-0.db-service.shop.svc.cluster.local
```
