# Create a VPC
resource "aws_vpc" "main" {
  cidr_block              = "10.0.0.0/16"
  enable_dns_hostnames     = true
}

# Create Subnet 1
resource "aws_subnet" "subnet_1" {
  vpc_id                  = aws_vpc.main.id      
  cidr_block              = "10.0.0.0/20"
  availability_zone       = "eu-west-2a"
  map_public_ip_on_launch = true 
}

# Create Subnet 2
resource "aws_subnet" "subnet_2" {
  vpc_id                  = aws_vpc.main.id      
  cidr_block              = "10.0.16.0/20" # Updated CIDR to prevent overlap with Subnet 1
  availability_zone       = "eu-west-2b"
  map_public_ip_on_launch = true
}

# Create Subnet 3
resource "aws_subnet" "subnet_3" {
  vpc_id                  = aws_vpc.main.id      
  cidr_block              = "10.0.32.0/20" # Updated CIDR to prevent overlap with Subnet 1
  availability_zone       = "eu-west-2c"
  map_public_ip_on_launch = true
}

# Create an Internet Gateway
resource "aws_internet_gateway" "internet_gw" {
  vpc_id = aws_vpc.main.id
}

# Create a Route Table
resource "aws_route_table" "route_table" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gw.id
  }

  route {
    cidr_block = "10.0.0.0/16"
    gateway_id = "local"
  }
}
 
resource "aws_route_table_association" "subnet_1_association" {
    subnet_id      = aws_subnet.subnet_1.id
    route_table_id = aws_route_table.route_table.id
}
resource "aws_route_table_association" "subnet_2_association" {
    subnet_id      = aws_subnet.subnet_2.id
    route_table_id = aws_route_table.route_table.id
}
resource "aws_route_table_association" "subnet_3_association" {
    subnet_id      = aws_subnet.subnet_3.id
    route_table_id = aws_route_table.route_table.id
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "devops-capstone-project"
  cluster_version = "1.27"

  cluster_endpoint_public_access = true

  vpc_id                   = aws_vpc.main.id
  subnet_ids               = [aws_subnet.subnet_1.id, aws_subnet.subnet_2.id, aws_subnet.subnet_3.id]
  control_plane_subnet_ids = [aws_subnet.subnet_1.id, aws_subnet.subnet_2.id, aws_subnet.subnet_3.id]

  eks_managed_node_groups = {
    green = {
      min_size       = 1
      max_size       = 1
      desired_size   = 1
      instance_types = ["t3.medium"]
    }
  }
}
