#!/bin/sh

APP_HOME=${APP_HOME:-"/app"}

mkdir -p $APP_HOME/log && touch $APP_HOME/log/flask.log

echo "$OPEN_D_PEM" > $APP_HOME/futu.pem

python $APP_HOME/app.py