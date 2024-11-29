provider "aws" {
  region = "ap-south-1"
}


module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_endpoint_public_access  = true
  cluster_name    = "spark-eks-granica"
  cluster_version = "1.27" 
  subnet_ids         = ["subnet-0b00fff3630f07792", "subnet-0036d60497f91fa6d", "subnet-08a5b4dbb53b04cc2"]
  vpc_id          = "vpc-0932ae17b32a1b8ee"
  eks_managed_node_groups = {
    spark = {
      instance_types = ["m5.xlarge"]

      min_size     = 4
      max_size     = 4
      desired_size = 4
    }
  }
}

resource "aws_db_instance" "hive_metastore_db" {
  allocated_storage    = 20
  engine               = "mysql"  
  engine_version       = "8.0"    
  instance_class       = "db.t3.micro"
  db_name                 = "hivemetastore"
  username             = "hive_test"
  password             = "hive_password"
  publicly_accessible  = true
  skip_final_snapshot  = true

  vpc_security_group_ids = ["sg-035bd8f28eca0a34c"]
  db_subnet_group_name      = "granica-test"
}

resource "aws_instance" "spark_driver" {
  ami           = "ami-0608ffd8c9c535658" # Image already having spark 3.5.1 setup
  instance_type = "m5.large"
  key_name      = "deepak-aws"         

  vpc_security_group_ids = ["sg-035bd8f28eca0a34c"]

  tags = {
    Name = "Spark-Driver"
  }
}

