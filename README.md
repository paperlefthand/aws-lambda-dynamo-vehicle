# aws-lambda-dynamo-vehicle

## 車両貸出管理システム

## TODO

- pantsでlambda build(zipをterraform下へ)->CLI apply
- `user_post`以外の関数のパッケージ化
- API Gatewayリソースの追加
- tfファイルの分割
- docker-composeでdynamo local/admin立ててpytest

```bash
poetry env use ~/.pyenv/versions/3.11.6/bin/python3.11
pants tailor ::
```

```bash
pants package src/vehicles/:lambda
unzip -l dist/lambda_vehicles.zip
mv dist/lambda_vehicles.zip ./terraform/
cd terraform && terraform plan  && terraform apply -auto-approve
```
