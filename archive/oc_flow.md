# delete 
oc delete all --all
oc delete pvc --all

remove nodePort: 30800 svc-a

oc apply -f k8s/

oc get pods
oc get svc
oc get statefulset
oc describe pod <pod-name>
oc logs <pod-name>
oc get svc server-b-service redis-svc
oc get pods -l app=server-b-label
oc get pods -l app=redis-label


oc expose service server-a-service
oc get routes