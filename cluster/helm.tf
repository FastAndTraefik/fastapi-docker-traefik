provider "helm" {
  kubernetes {
    host                   = aws_eks_cluster.prod-eks-cluster.endpoint
    cluster_ca_certificate = base64decode(aws_eks_cluster.prod-eks-cluster.certificate_authority[0].data)
    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      args        = ["eks", "get-token", "--cluster-name", aws_eks_cluster.prod-eks-cluster.name]
      command     = "aws"
    }
  }
}


resource "helm_release" "aws_load_balancer_controller"{
  name = "aws-load-balancer-controller"
  repository = "https://aws.github.io/eks-charts"
  chart = "aws-load-balancer-controller"
  namespace = "kube-system"

  set {
    name = "replicaCount"
    value = 1
  }

  set{
    name = "clusterName"
    value = aws_eks_cluster.prod-eks-cluster.name
  }

  set{
    name="vpcId"
    value = aws_vpc.eks-cluster-vpc.id
  }

  set{
    name = "serviceAccount.name"
    value= "aws-load-balancer-controller"
  }

  set{
    name= "serviceAccount.annotations.eks\\.amazonaws\\.com/role-arn"
    value = aws_iam_role.ingress-role.arn
  }
}
