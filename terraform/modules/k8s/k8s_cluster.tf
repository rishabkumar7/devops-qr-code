resource "aws_eks_cluster" "qrcode_eks_cluster" {
  name = "qrcode_eks_cluster"

  access_config {
    authentication_mode = "API"
  }

  role_arn = aws_iam_role.qrcode_eks_cluster_role.arn
  version  = "1.31"

  vpc_config {
    subnet_ids = [var.subnet_A_id, var.subnet_B_id]
  }

  # Ensure that IAM Role permissions are created before and deleted
  # after EKS Cluster handling. Otherwise, EKS will not be able to
  # properly delete EKS managed EC2 infrastructure such as Security Groups.
  depends_on = [
    aws_iam_role_policy_attachment.qrcode_cluster_role_policy
  ]
}

resource "aws_iam_role" "qrcode_eks_cluster_role" {
  name = "qrcode_eks_cluster_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "sts:AssumeRole",
          "sts:TagSession"
        ]
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "qrcode_cluster_role_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.qrcode_eks_cluster_role.name
}