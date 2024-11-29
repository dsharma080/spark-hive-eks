@echo off

REM Define MySQL credentials
SET MYSQL_USER=hive_test
SET MYSQL_PASSWORD=hive_password
SET DATABASE_NAME=hivemetastore

mysql -u %MYSQL_USER% -h %RDS_ENDPOINT% -p%MYSQL_PASSWORD% -D %DATABASE_NAME% -e "source mysql/hive-schema-3.0.0.mysql.sql"
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to create schema 3.0.0. Exiting.
    exit /b %ERRORLEVEL%
)
echo Created schema 3.0.0 

mysql -u %MYSQL_USER% -h %RDS_ENDPOINT% -p%MYSQL_PASSWORD% -D %DATABASE_NAME% -e "source mysql/upgrade-3.0.0-to-3.1.0.mysql.sql"
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to upgrade schema to 3.1.0. Exiting.
    exit /b %ERRORLEVEL%
)
echo Upgraded schema to 3.1.0 
echo RDS schema setup successfully.
