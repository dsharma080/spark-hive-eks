@echo off

echo Initializing Terraform...
terraform init
IF ERRORLEVEL 1 (
    echo Terraform initialization failed. Exiting.
    exit /b 1
)

echo Validating Terraform configuration...
terraform validate
IF ERRORLEVEL 1 (
    echo Terraform validation failed. Exiting.
    exit /b 1
)

REM Create a Terraform plan
echo Generating Terraform plan...
terraform plan -out=tfplan
IF ERRORLEVEL 1 (
    echo Terraform plan generation failed. Exiting.
    exit /b 1
)

REM Prompt user to apply the plan
set /p APPLY="Do you want to apply the Terraform plan? (yes/no): "
if /i "%APPLY%"=="yes" (
    echo Applying Terraform plan...
    terraform apply "tfplan"
    IF ERRORLEVEL 1 (
        echo Terraform apply failed. Exiting.
        exit /b 1
    )
    echo Terraform apply completed successfully!
) else (
    echo Terraform apply skipped.
)

REM Clean up the plan file
del tfplan

REM Script completed
echo Terraform setup completed.


REM Run the Python script
echo Updating security group permissions 

python update_perms.py 

REM Check the exit code of the Python script
IF %ERRORLEVEL% NEQ 0 (
    echo The Python script update_perms.py encountered an error. Exiting.
    exit /b %ERRORLEVEL%
)

echo Security group permissions updated successfully!
