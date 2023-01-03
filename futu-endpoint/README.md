# Docker FutuOpenD Endpoint

This docker container aims to create FutuOpenD as endpoint to communicate with Webhook side. The container compatible with Mac M1 arm.

## How to run

1. Download Ubuntu version of FutuOpenD from [LINK](https://www.futunn.com/en/download/OpenAPI) and copy all files to /src

2. Run below command to build container and run

```
$ docker build -t py-futu-opend .

$ docker run --platform=linux/x86_64 -d -t -i -e FUTU_LOGIN_ACCOUNT='YOUR_FUTU_ACCOUNT' -e FUTU_LOGIN_PASSWORD_HASH='YOUR_PASSWORD_HASH' -p 11111:11111 -p 22222:22222 -p 33333:33333 --name py-futu-opend py-futu-opend
```

3. If phone verification required

```
<!-- To Check Container ID of py-futu-opend -->
$ docker ps

<!-- Paste the container id -->
$ docker attach [CONTAINER_ID]

$ input_phone_verify_code -code=[YOUR_SIX_DIGITS_CODE]
```

4. Go to cmd shell in docker and copy pem secret

```
$ cat futu.pem
```
