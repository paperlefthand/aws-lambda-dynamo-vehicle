terraform {
  cloud {
    organization = "miulab"

    workspaces {
      name = "vehicle-rental"
    }
  }

  required_version = ">= 1.1.2"
}