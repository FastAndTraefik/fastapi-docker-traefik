# NAT.tf
resource "aws_eip" "nat-ip" {
  domain      = "vpc"
}
resource "aws_nat_gateway" "my-nat-gateway" {
  allocation_id = aws_eip.nat-ip.id
  subnet_id     = aws_subnet.public-east-1b.id

  tags = {
    Name = "gw NAT"
  }

  depends_on = [aws_internet_gateway.gw]
}
