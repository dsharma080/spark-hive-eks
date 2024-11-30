@echo off
REM set RDS_ENDPOINT=your_rds_endpoint_here

REM Run Python script to generate hive configuration
echo Running Python script to generate hive configuration...
python generate_hive_site.py
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to execute generate_hive_site.py. Exiting.
    exit /b %ERRORLEVEL%
)

REM Run Python script to generate hive deployment configuration
echo Running Python script to generate hive deployment configuration...
python generate_hive_metastore_deployment.py
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to execute generate_hive_metastore_deployment.py. Exiting.
    exit /b %ERRORLEVEL%
)

REM Build Docker image
echo Building Docker image...
docker build -t dsharma080/hive-metastore:latest .
IF %ERRORLEVEL% NEQ 0 (
    echo Docker build failed. Exiting.
    exit /b %ERRORLEVEL%
)

REM Push Docker image to Docker Hub
echo Pushing Docker image to Docker Hub...
docker push dsharma080/hive-metastore:latest
IF %ERRORLEVEL% NEQ 0 (
    echo Docker push failed. Exiting.
    exit /b %ERRORLEVEL%
)

REM Apply Kubernetes deployment configuration
echo Applying Kubernetes deployment configuration...
kubectl apply -f k8/hive-metastore-deployment.yaml
IF %ERRORLEVEL% NEQ 0 (
    echo Kubernetes deployment apply failed. Exiting.
    exit /b %ERRORLEVEL%
)

REM Apply Kubernetes service configuration
echo Applying Kubernetes service configuration...
kubectl apply -f k8/hive-metastore-service.yaml
IF %ERRORLEVEL% NEQ 0 (
    echo Kubernetes service apply failed. Exiting.
    exit /b %ERRORLEVEL%
)

echo Hive setup executed successfully.
