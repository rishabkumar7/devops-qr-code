resource "aws_eks_node_group" "qrcode_node_group" {
  cluster_name    = aws_eks_cluster.qrcode_eks_cluster.name
  node_group_name = "qrcode_node_group"
  node_role_arn   = aws_iam_role.qrcode_eks_node_role.arn
  subnet_ids      = [var.subnet_A_id, var.subnet_B_id]

  scaling_config {
    desired_size = 1
    max_size     = 2
    min_size     = 1
  }

  update_config {
    max_unavailable = 1
  }

  # Ensure that IAM Role permissions are created before and deleted after EKS Node Group handling.
  # Otherwise, EKS will not be able to properly delete EC2 Instances and Elastic Network Interfaces.
  depends_on = [
    aws_iam_role_policy_attachment.qrcode_EKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.qrcode_EKS_CNI_Policy,
    aws_iam_role_policy_attachment.qrcode_EC2ContainerRegistryReadOnly,
  ]
}

resource "aws_iam_role" "qrcode_eks_node_role" {
  name = "qrcode_eks_node_role"

  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
    Version = "2012-10-17"
  })
}

resource "aws_iam_role_policy_attachment" "qrcode_EKSWorkerNodePolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.qrcode_eks_node_role.name
}

resource "aws_iam_role_policy_attachment" "qrcode_EKS_CNI_Policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.qrcode_eks_node_role.name
}

resource "aws_iam_role_policy_attachment" "qrcode_EC2ContainerRegistryReadOnly" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.qrcode_eks_node_role.name
}