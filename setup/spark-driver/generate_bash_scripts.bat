@echo off

echo Running generate_spark_submit.py...
python generate_spark_submit.py
if %ERRORLEVEL% neq 0 (
    echo Error: generate_spark_submit.py failed.
    exit /b 1
)

echo Running generate_spark_sql.py...
python generate_spark_sql.py
if %ERRORLEVEL% neq 0 (
    echo Error: generate_spark_sql.py failed.
    exit /b 1
)

echo Spark driver scripts generated successfully