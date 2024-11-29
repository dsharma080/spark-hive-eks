@echo off
REM Set AWS region and EKS cluster name
SET REGION=ap-south-1
SET CLUSTER_NAME=spark-eks-test

REM Update kubeconfig for the EKS cluster
echo Updating kubeconfig for EKS cluster: %CLUSTER_NAME% in region: %REGION%...
aws eks --region %REGION% update-kubeconfig --name %CLUSTER_NAME%
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to update kubeconfig. Exiting.
    exit /b %ERRORLEVEL%
)
echo kubeconfig updated successfully.

REM Apply Kubernetes deployment from spark.yaml
echo Applying spark.yaml...
kubectl apply -f spark.yaml
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to apply spark.yaml. Exiting.
    exit /b %ERRORLEVEL%
)
echo spark.yaml applied successfully.

echo Waiting 30 seconds for Spark deployment to stabilize...
timeout /t 30 /nobreak

REM Apply Kubernetes service from spark-master-service.yaml
echo Applying spark-master-service.yaml...
kubectl apply -f spark-master-service.yaml
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to apply spark-master-service.yaml. Exiting.
    exit /b %ERRORLEVEL%
)
echo spark-master-service.yaml applied successfully.

echo Spark setup executed successfully.
