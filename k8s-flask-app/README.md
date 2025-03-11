# Kubernetes Flask PostgreSQL Deployment

This repository contains Kubernetes manifests for deploying a Flask web application with a PostgreSQL database on a Minikube cluster.

## Project Structure

```
k8s-flask-app/
│── manifests/
│   │── deployment/
│   │   │── flask-deployment.yaml
│   │   │── postgres-deployment.yaml
│   │── service/
│   │   │── flask-service.yaml
│   │   │── postgres-service.yaml
│   │── configmap/
│   │   │── postgres-configmap.yaml
│   │── secret/
│   │   │── postgres-secret.yaml
│   │── autoscaling/
│   │   │── flask-hpa.yaml
│── app/
│   │── Dockerfile
│   │── requirements.txt
│   │── app.py
│── README.md
│── submission/
    │── (screenshots and deployment details)
```

## Deployment Steps

### 1. Start Minikube

```bash
minikube start --driver=docker
```

### 2. Build the Flask Application Docker Image

```bash
# Set docker to use minikube's docker daemon
eval $(minikube docker-env)

# Build the Docker image
cd k8s-flask-app/app
docker build -t flask-postgres-app:latest .
```

### 3. Apply Kubernetes Manifests

```bash
# Apply ConfigMap and Secret first
kubectl apply -f ../manifests/configmap/postgres-configmap.yaml
kubectl apply -f ../manifests/secret/postgres-secret.yaml

# Apply PostgreSQL Deployment and Service
kubectl apply -f ../manifests/deployment/postgres-deployment.yaml
kubectl apply -f ../manifests/service/postgres-service.yaml

# Wait for PostgreSQL to be ready
kubectl wait --for=condition=available deployment/postgres --timeout=120s

# Apply Flask App Deployment and Service
kubectl apply -f ../manifests/deployment/flask-deployment.yaml
kubectl apply -f ../manifests/service/flask-service.yaml

# Optional: Apply HorizontalPodAutoscaler for the Flask application
kubectl apply -f ../manifests/autoscaling/flask-hpa.yaml
```

### 4. Access the Application

```bash
# Get the URL to access the Flask application
minikube service flask-app --url
```

## Testing Database Connectivity

Access the `/db-test` endpoint to verify database connectivity.

## Scaling Replicas

To manually scale the Flask application:

```bash
# Scale up
kubectl scale deployment/flask-app --replicas=4

# Scale down
kubectl scale deployment/flask-app --replicas=1
```

If you've applied the HorizontalPodAutoscaler, the application will automatically scale between min and max replicas based on CPU utilization.

## Investigating Replicas

For the exercise requirements related to investigating min and max replicas:

1. Min and max replicas are defined in the HorizontalPodAutoscaler configuration:
   - Min replicas: 1
   - Max replicas: 5
   - Scaling trigger: 70% CPU utilization

2. You can observe scaling behavior with:
   ```bash
   # Watch the HPA status
   kubectl get hpa flask-app-hpa --watch
   
   # Generate load to trigger scaling
   # (You could use a tool like 'hey' or 'ab' for this)
   ```

## Cleanup

```bash
# Delete all resources
kubectl delete -f ../manifests/autoscaling/
kubectl delete -f ../manifests/deployment/
kubectl delete -f ../manifests/service/
kubectl delete -f ../manifests/configmap/
kubectl delete -f ../manifests/secret/
```