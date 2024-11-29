@echo off

:: Set the environment variables (make sure they are set beforehand or pass them as arguments)
set PPK_FILE=%PPK_FILE%
set SPARKDRIVER_IP=%SPARKDRIVER_IP%

:: Check if the environment variables are set
if "%PPK_FILE%"=="" (
    echo Error: PPK_FILE environment variable is not set.
    exit /b 1
)

if "%SPARKDRIVER_IP%"=="" (
    echo Error: SPARKDRIVER_IP environment variable is not set.
    exit /b 1
)

:: Copy multiple files in one pscp command
pscp -i "%PPK_FILE%" ^
    ../../data-pipeline/log-parser/target/scala-2.12/log-parser-assembly-1.0.jar ^
    spark_submit_script.sh ^
    spark_sql_script.sh ^
    ubuntu@%SPARKDRIVER_IP%:/home/ubuntu

:: Verify if the copy command was successful
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to copy files.
    exit /b 1
)

echo Files copied successfully.
