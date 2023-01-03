#!/bin/sh

FUTU_HOME=${FUTU_HOME:-"/FutuOpenD"}

openssl genrsa -out $FUTU_HOME/futu.pem 1024

cat $FUTU_HOME/futu.pem

sed -i "s/FUTU_LOGIN_ACCOUNT/$FUTU_LOGIN_ACCOUNT/g" $FUTU_HOME/FutuOpenD.xml
sed -i "s/FUTU_LOGIN_PASSWORD_HASH/$FUTU_LOGIN_PASSWORD_HASH/g" $FUTU_HOME/FutuOpenD.xml
sed -i "s|RSA_PATH|$FUTU_HOME/futu.pem|g" $FUTU_HOME/FutuOpenD.xml

cfg_file=${cfg_file:-"$FUTU_HOME/FutuOpenD.xml"}

OPTS="-cfg_file=$cfg_file "

echo "OPTS: $OPTS $EXOPT"

$FUTU_HOME/FutuOpenD $OPTS $EXOPT
