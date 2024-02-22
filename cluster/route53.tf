# route53.tf
# create a route53 hosted zone
resource "aws_route53_zone" "main" {
  name = "final-project.devops-fairy.cloudns.biz"
}

# attach records to it
resource "aws_route53_record" "main" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "final-project.devops-fairy.cloudns.biz"
  type    = "CNAME"
  ttl     = "300"
  records = ["dualstack.k8s-default-prodk8sa-ddb4bf0a73-1855298043.us-east-1.elb.amazonaws.com"]
}
