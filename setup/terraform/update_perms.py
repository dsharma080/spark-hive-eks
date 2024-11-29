import boto3

# Configuration
AWS_REGION = "ap-south-1"  # Replace with your AWS region

# Initialize boto3 client
ec2_client = boto3.client("ec2", region_name=AWS_REGION)

def get_all_security_groups():
    """
    Retrieve all security groups in the AWS account for the specified region.
    """
    security_groups = []
    paginator = ec2_client.get_paginator("describe_security_groups")
    for page in paginator.paginate():
        for sg in page["SecurityGroups"]:
            security_groups.append(sg["GroupId"])
    return security_groups

def authorize_all_tcp(sg_id):
    """
    Authorize all inbound and outbound TCP traffic for a security group.
    """
    try:
        # Authorize inbound TCP traffic
        ec2_client.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": 0,
                    "ToPort": 65535,
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
                }
            ]
        )
        print(f"Inbound TCP traffic allowed for Security Group: {sg_id}")
    except Exception as e:
        if "already exists" in str(e):
            print(f"Inbound TCP traffic already allowed for Security Group: {sg_id}")
        else:
            print(f"Error authorizing inbound TCP traffic for {sg_id}: {e}")

    try:
        # Authorize outbound TCP traffic
        ec2_client.authorize_security_group_egress(
            GroupId=sg_id,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": 0,
                    "ToPort": 65535,
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
                }
            ]
        )
        print(f"Outbound TCP traffic allowed for Security Group: {sg_id}")
    except Exception as e:
        if "already exists" in str(e):
            print(f"Outbound TCP traffic already allowed for Security Group: {sg_id}")
        else:
            print(f"Error authorizing outbound TCP traffic for {sg_id}: {e}")

def main():
    try:
        security_groups = get_all_security_groups()
        print(f"Found {len(security_groups)} security groups in AWS account.")
        for sg_id in security_groups:
            print(f"Processing Security Group: {sg_id}")
            authorize_all_tcp(sg_id)
    except Exception as e:
        print(f"Error processing security groups: {e}")

if __name__ == "__main__":
    main()
