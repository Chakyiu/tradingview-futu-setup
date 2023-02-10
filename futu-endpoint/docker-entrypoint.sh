#!/bin/sh

FUTU_HOME=${FUTU_HOME:-"/FutuOpenD"}

openssl genrsa -out $FUTU_HOME/futu.pem 1024

cat $FUTU_HOME/futu.pem

cfg_file=${cfg_file:-"$FUTU_HOME/FutuOpenD.xml"}

sed -i "s/<login_account>100000<\/login_account>/<login_account>$FUTU_LOGIN_ACCOUNT<\/login_account>/g" $cfg_file
sed -i "s/<!-- <login_pwd_md5>6e55f158a827b1a1c4321a245aaaad88<\/login_pwd_md5> -->/<login_pwd_md5>$FUTU_LOGIN_PASSWORD_HASH<\/login_pwd_md5>/g" $cfg_file
sed -i "s|<!-- <rsa_private_key>~\/rsa<\/rsa_private_key> -->|<rsa_private_key>$FUTU_HOME\/futu\.pem<\/rsa_private_key>|g" $cfg_file

OPTS="-cfg_file=$cfg_file "

echo "OPTS: $OPTS $EXOPT"

$FUTU_HOME/FutuOpenD $OPTS $EXOPT
