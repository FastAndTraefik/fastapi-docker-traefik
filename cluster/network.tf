# network.tf
resource "aws_vpc" "eks-cluster-vpc" {
  cidr_block = "10.0.0.0/16"
}
# network.tf
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.eks-cluster-vpc.id

  tags = {
    Name = "main-ig-gateway"
  }
}
# network.tf
resource "aws_subnet" "private-east-1a" {
  vpc_id     = aws_vpc.eks-cluster-vpc.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "us-east-1a-private"
    "kubernetes.io/role/internal-elb" = 1
    "kubernetes.io/cluster/eks-cluster-production" = "shared"
  }
}


resource "aws_subnet" "public-east-1b" {
  vpc_id     = aws_vpc.eks-cluster-vpc.id
  cidr_block = "10.0.2.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "us-east-1b-public"
    "kubernetes.io/role/elb" = 1
    "kubernetes.io/cluster/eks-cluster-production" = "shared"
  }
}
resource "aws_subnet" "public-east-1a" {
  vpc_id     = aws_vpc.eks-cluster-vpc.id
  cidr_block = "10.0.3.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "us-east-1a-public"
    "kubernetes.io/role/elb" = 1
    "kubernetes.io/cluster/eks-cluster-production" = "shared"
  }
}
resource "aws_subnet" "private-east-1b" {
  vpc_id     = aws_vpc.eks-cluster-vpc.id
  cidr_block = "10.0.4.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "us-east-1b-private"
    "kubernetes.io/role/internal-elb" = 1
    "kubernetes.io/cluster/eks-cluster-production" = "shared"
  }
}

