# Kubernetes MLOps

## Build a simple ML app using Flask

```bash
# Build Docker image
docker build --tag tungdao17/test-ml-score-api py-flask-ml-score-api
# Test
docker run --rm --name test-api -p 5000:5000 -d tungdao17/test-ml-score-api
docker ps
# curl test: this should returns {"score":[1,2]}
curl http://localhost:5000/score \
    --request POST \
    --header "Content-Type: application/json" \
    --data '{"X": [1, 2]}'
docker stop test-api
# Push Docker image
docker login
docker push tungdao17/test-ml-score-api
```

## Deploy the simple ML app to local Kubernetes

```bash
# Create a deployment
kubectl create deploy test-ml-score-api --image=tungdao17/test-ml-score-api:latest
# Check the status
kubectl rollout status deploy test-ml-score-api
# Check pods
kubectl get pod
# Test our container inside deployed pod
# Replace test-ml-score-api-79f7f56f88-h28bv with the pod name
kubectl port-forward test-ml-score-api-79f7f56f88-h28bv 5000:5000
# curl test: this should returns {"score":[1,2]}
curl http://localhost:5000/score \
    --request POST \
    --header "Content-Type: application/json" \
    --data '{"X": [1, 2]}'
# Expose the service as a Load Balancer service in local
# This requires the service type LoadBalancer provided
# We can install it in local by using k8s nginx ingress controller (https://kubernetes.github.io/ingress-nginx/deploy/) and MetalLB (https://metallb.universe.tf/concepts/)
kubectl expose deploy test-ml-score-api --port 5000 --type=LoadBalancer --name test-ml-score-api-lb
# Check LoadBalancer service's external-ip, assume it is 10.121.177.41
kubectl get svc
# curl test
curl http://10.121.177.41:5000/score \
    --request POST \
    --header "Content-Type: application/json" \
    --data '{"X": [1, 2]}'
# Clean resources
kubectl delete svc test-ml-score-api-lb
kubectl delete deploy test-ml-score-api
```

## Deploy the simple ML app to EKS

```bash
# Install eksctl, kubectl in your local env
# Init a cluster in EKS. This might take 15m
# This will auto-switch to the EKS context
eksctl create cluster --name k8s-test-cluster --without-nodegroup
# Create a nodegroup. This might take 5m
eksctl create nodegroup --cluster k8s-test-cluster --node-type t2.small --nodes 3
# Verify kubectl context = EKS context
kubectl config get-contexts
# To switch to local context, run
kubectl config use-context <local-context-name>

# Create a deployment
kubectl create deploy test-ml-score-api --image=tungdao17/test-ml-score-api:latest
# Expose the deployment
kubectl expose deploy test-ml-score-api --port 5000 --type=LoadBalancer --name test-ml-score-ap
i-lb
# Check LoadBalancer service's external-ip, it will be a domain like *.amazonaws.com
kubectl get svc
# curl test, replace <domain> with your one
curl http://<domain>:5000/score \
    --request POST \
    --header "Content-Type: application/json" \
    --data '{"X": [1, 2]}'
# Alternatively, you can use Postman or Thunder Client extension in vscode
# Clean resources
kubectl delete svc test-ml-score-api-lb
kubectl delete deploy test-ml-score-api
```

## Deploy to EKS using YAML files

```bash
# Create resources
kubectl apply -f py-flask-ml-score-api/py-flask-ml-score.yaml
# Check resources
kubectl get all -n test-ml-app
# Set default namespace for current context if you want
kubectl config set-context --current -n <namespace>
# Perform LoadBalancer service test same as the previous section
# Clean resources
kubectl delete -f py-flask-ml-score-api/py-flask-ml-score.yaml
```

## Deploy to EKS using Helm

```bash
# Install Helm
# Install app dry run
helm install helm-ml-score-app --debug --dry-run --generate-name
# Install
helm install test-ml-app helm-ml-score-app
# Check Helm chart
helm list
helm status test-ml-app
# Perform LoadBalancer service test same as the previous section
# Clean resources
helm delete test-ml-app
```
