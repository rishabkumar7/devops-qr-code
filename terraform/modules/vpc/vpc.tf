
# VPC creation
resource "aws_vpc" "qrcode_vpc" {
  cidr_block = "10.0.0.0/16"
}

# creation of two subnets
resource "aws_subnet" "qrcode_subnet_A" {
  vpc_id     = aws_vpc.qrcode_vpc.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "us-east-1a"
}

resource "aws_subnet" "qrcode_subnet_B" {
  vpc_id     = aws_vpc.qrcode_vpc.id
  cidr_block = "10.0.2.0/24"
  availability_zone = "us-east-1b"
}

# creation of internet gateway so the subnets have access to internet and can be accessed from internet
resource "aws_internet_gateway" "qrcode_ig" {
  vpc_id = aws_vpc.qrcode_vpc.id
}

# route table to route traffic destined for internet to internet gateway
resource "aws_route_table" "qrcode_rt" {
  vpc_id = aws_vpc.qrcode_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.qrcode_ig.id
  }
}

# associate route table with both subnets
resource "aws_route_table_association" "qrcode_rt_assoc_A" {
  subnet_id      = aws_subnet.qrcode_subnet_A.id
  route_table_id = aws_route_table.qrcode_rt.id
}

resource "aws_route_table_association" "qrcode_rt_assoc_B" {
  subnet_id      = aws_subnet.qrcode_subnet_B.id
  route_table_id = aws_route_table.qrcode_rt.id
}