resource "aws_dynamodb_table" "vehicle_record" {
  name           = "VehicleRecord"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "VehicleId"

  attribute {
    name = "VehicleId"
    type = "S"
  }

}
