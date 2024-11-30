import os
import yaml

def generate_yaml():
    # Get the RDS_ENDPOINT environment variable
    rds_endpoint = os.getenv("RDS_ENDPOINT")
    if not rds_endpoint:
        raise EnvironmentError("RDS_ENDPOINT environment variable is not set.")

    # Construct the YAML structure
    deployment_yaml = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": "hive-metastore",
        },
        "spec": {
            "replicas": 1,
            "selector": {
                "matchLabels": {
                    "app": "hive-metastore",
                },
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": "hive-metastore",
                    },
                },
                "spec": {
                    "containers": [
                        {
                            "name": "hive-metastore",
                            "image": "dsharma080/hive-metastore:latest",
                            "ports": [
                                {"containerPort": 9083}
                            ],
                            "env": [
                                {
                                    "name": "METASTORE_DB_URL",
                                    "value": f"jdbc:mysql://{rds_endpoint}:3306/hivemetastore",
                                },
                                {"name": "METASTORE_DB_USER", "value": "granica_test"},
                                {"name": "METASTORE_DB_PASSWORD", "value": "granica_password"},
                            ],
                        }
                    ],
                },
            },
        },
    }

    # Write the YAML to a file
    with open("k8/hive-metastore-deployment.yaml", "w") as yaml_file:
        yaml.dump(deployment_yaml, yaml_file, default_flow_style=False)

    print("YAML file 'hive-metastore-deployment.yaml' has been generated successfully.")

if __name__ == "__main__":
    try:
        generate_yaml()
    except Exception as e:
        print(f"Error: {e}")
