
module "qrcode_vpc_config"{
  source = "./modules/vpc"
}

module "qrcode_k8s" {
  source = "./modules/k8s"
  
  # Pass the subnets to the k8s module
  subnet_A_id = module.qrcode_vpc_config.subnet_A_id
  subnet_B_id = module.qrcode_vpc_config.subnet_B_id
}