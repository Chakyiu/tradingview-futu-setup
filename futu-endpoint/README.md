# Docker FutuOpenD Endpoint

This docker container aims to create FutuOpenD as endpoint to communicate with Webhook side. The container compatible with Mac M1 arm.

## How to run

1. Download Ubuntu version of FutuOpenD from [LINK](https://www.futunn.com/en/download/OpenAPI) and copy all files to /src

2. Run below command to build container and run

```
$ md5 -s YOUR_PASSWORD
# Copy the hash, example result would be:
# MD5("YOUR_PASSWORD") = YOUR_PASSWORD_HASH


# Standard amd64 environment
$ docker build -t py-futu-opend -f ./Dockerfile .

$ docker run -d -t -i -e FUTU_LOGIN_ACCOUNT='YOUR_FUTU_ACCOUNT' -e FUTU_LOGIN_PASSWORD_HASH='YOUR_PASSWORD_HASH' -p 11111:11111 -p 22222:22222 -p 33333:33333 --name py-futu-opend py-futu-opend

# Running under Mac M1/M2 environment
$ docker build -t py-futu-opend -f ./Dockerfile.x86_64 .

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

## Change Log

- 2023-01-03
  - Project Init
- 2023-01-04
  - Update LICENSE
- 2023-02-11
  - Update user guide
  - Update bash script to automatically update account info
