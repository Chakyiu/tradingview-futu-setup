# pylint: disable-all
from flask import Flask, request
import json
import telegram
import os
import requests
import time
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning
import logging
import pytz
from futu import *

logging.basicConfig(filename='./log/flask.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %('f'name)s %(threadName)s : %(message)s')
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

app = Flask(__name__)

rsa_path = os.path.dirname(os.path.abspath(__file__)) + '/futu.pem'

SysConfig.enable_proto_encrypt(is_encrypt=True)
SysConfig.set_init_rsa_file(rsa_path)

ORDER_PLACE_ATTEMPT = 4


@app.route("/")
def health():
    return "OK"


def placeOrder(trd_ctx, price, qty, code, trade_side, trade_env, order_type, order_time):
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    bot = telegram.Bot(telegram_token) if telegram_token != None else None

    order_success_message = ""
    _order_time_utc = datetime.strptime(
        order_time, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
    _order_time_est = _order_time_utc.astimezone(pytz.timezone('US/Eastern'))

    app.logger.info(
        f'Detected Time in UTC {_order_time_utc} | Detected Time in EST {_order_time_est}')

    for attempt in range(1, ORDER_PLACE_ATTEMPT):
        app.logger.info(f'Placing Order: Attempt {attempt}')
        err_msg = None
        try:
            order_ret, order_data = None, None
            # Good until cancel order when after the market
            if _order_time_est.hour >= 16 and _order_time_est.hour <= 23:
                order_ret, order_data = trd_ctx.place_order(
                    price=price, qty=qty, code=code, trd_side=trade_side, trd_env=trade_env, order_type=OrderType.NORMAL, time_in_force=TimeInForce.GTC)
                if order_ret == RET_OK:
                    order_success_message += "Warning!!! After the market order placed, order may not be executed\n"
            else:
                order_ret, order_data = trd_ctx.place_order(
                    price=price, qty=qty, code=code, trd_side=trade_side, trd_env=trade_env, order_type=order_type)

            if order_ret == RET_OK:
                order_success_message += "%s %s %s@%s" % (str(order_data['code'][0]), str(
                    order_data['trd_side'][0]), str(price), str(order_data['qty'][0]))
                app.logger.info("Order Place: %s" % order_success_message)
            else:
                raise Exception(order_data)
            return order_data, order_success_message
        except Exception as e:
            err_msg = f'Error: {e}, Attempt: {attempt}'
            app.logger.error(err_msg)
            if bot:
                bot.send_message(text=err_msg, chat_id=telegram_chat_id)
            time.sleep(1)
            continue

    app.logger.error(f'Failed to place Order')
    return err_msg, None


@app.route("/webhook", methods=['POST'])
def webhook():

    app.logger.info('===============================================')

    # Kill when no request data
    if not request.data:
        app.logger.info('Error, No Request Data')

        return json.dumps({
            "code": "error",
            "message": "No data"
        })

    data = json.loads(request.data)
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    bot = telegram.Bot(telegram_token) if telegram_token != None else None

    is_auto = data['is_auto']
    symbol = data['ticker']
    market = data['market']
    order_time = data['time']
    code = "%s.%s" % (market, symbol)
    trade_side = TrdSide.BUY if data['strategy']['order_action'] == 'buy' else TrdSide.SELL
    opposite_trade_side = TrdSide.BUY if trade_side == TrdSide.SELL else TrdSide.SELL
    qty = float(data['strategy']['order_contracts'])
    price = float(data['strategy']['order_price'])
    market_position = data['strategy']['market_position']
    market_position_size = float(data['strategy']['market_position_size'])
    prev_market_position = data['strategy']['prev_market_position']
    prev_market_position_size = float(
        data['strategy']['prev_market_position_size'])

    trade_market = TrdMarket.US if data['market'] == 'US' else TrdMarket.HK
    trade_env = TrdEnv.REAL if data['environment'] == 'REAL' else TrdEnv.SIMULATE
    order_type = OrderType.MARKET if trade_env == TrdEnv.REAL else OrderType.NORMAL
    securities_firm = SecurityFirm.FUTUSECURITIES
    currency = Currency.USD if data['currency'] == 'USD' else Currency.HKD
    trading_pwd = os.getenv('TRADING_PWD')
    host = os.getenv('OPEN_D_HOST')
    port = int(os.getenv('OPEN_D_PORT'))

    app.logger.info('Order detected: %s', json.dumps(data))

    message = ""
    tg_message = ""
    if data['passphrase'] != os.getenv('WEBHOOK_PASSPHRASE'):
        app.logger.error('Webhook Passphrase Error: %s', json.dumps(data))
        message = json.dumps({
            "code": "error",
            "error": "Webhook Passphrase Error",
            "message": json.loads(request.data)
        })

        if bot:
            bot.send_message(text=message, chat_id=telegram_chat_id)
        return message

    if is_auto:
        trd_ctx = None
        try:
            trd_ctx = OpenSecTradeContext(filter_trdmarket=trade_market, host=host,
                                          port=port, is_encrypt=None, security_firm=securities_firm)
            if trade_env == TrdEnv.REAL:
                unlock_ret, unlock_data = trd_ctx.unlock_trade(trading_pwd)
                if unlock_ret == RET_OK:
                    app.logger.info("Unlock Trade Success")
                else:
                    app.logger.error("Unlock Trade Failed", unlock_data)
                    raise Exception('Unlock Trade Failed', unlock_data)

            long_power = 0
            short_power = 0
            acct_ret, acct_data = trd_ctx.accinfo_query(
                trd_env=trade_env, currency=currency)
            if acct_ret == RET_OK:
                long_power = float(
                    acct_data['cash'][0] if acct_data['cash'][0] != 'N/A' else 0)
                short_power = float(
                    acct_data['max_power_short'][0] if acct_data['max_power_short'][0] != 'N/A' else 0)
                app.logger.info("Long Power: %s\tShort Power: %s" %
                                (str(long_power), str(short_power)))
            else:
                raise Exception("Unable to Fetch Acct Info: ", acct_data)

            position_qty = 0
            position_ret, position_data = trd_ctx.position_list_query(
                code=code, trd_env=trade_env)
            if position_ret == RET_OK:
                position_qty = abs(float(
                    position_data['qty'][0])) if len(position_data['qty'].values.tolist()) > 0 else 0.0
            else:
                raise Exception(
                    "Unable to Fetch Position data: ", position_data)

            app.logger.info("Detected Position: %s" % position_qty)

            success_message = ""
            # From Flat to Long/ Short
            if prev_market_position == 'flat':
                app.logger.info('Order Buy from %s to %s',
                                prev_market_position, market_position)

                if trade_side == TrdSide.BUY and qty * price > long_power:
                    raise Exception("[Invalid Long Power]: Current Long Power: %s | Power Needed: %s" % (
                        long_power, qty * price))
                if trade_side == TrdSide.SELL and abs(qty * price) > short_power:
                    raise Exception("[Invalid Shorting Power]: Current Buying Power: %s | Power Needed: %s" % (
                        short_power, abs(qty * price)))

                order_data, order_success_message = placeOrder(
                    trd_ctx=trd_ctx, price=price, qty=qty, code=code, trade_side=trade_side, trade_env=trade_env, order_type=order_type, order_time=order_time)

                if order_success_message:
                    success_message = order_success_message
                else:
                    raise Exception("Unable to Place Order: %s" % order_data)

            # From Long/ Short to Same Position
            elif prev_market_position == market_position:
                app.logger.info('Order Buy from %s to %s',
                                prev_market_position, market_position)

                if position_qty == 0 or abs(qty) > abs(position_qty):
                    raise Exception("[Invalid Order from %s to %s]: Current Position: %s | Qty to Order: %s | Order Action: %s" % (
                        prev_market_position, market_position, str(position_qty), str(qty), trade_side))

                order_data, order_success_message = placeOrder(
                    trd_ctx=trd_ctx, price=price, qty=qty, code=code, trade_side=trade_side, trade_env=trade_env, order_type=order_type, order_time=order_time)

                if order_success_message:
                    success_message = order_success_message
                else:
                    raise Exception("Unable to Place Order: %s" % order_data)

            # From Long/ Short to Flat
            elif market_position == 'flat':
                app.logger.info('Order Buy from %s to %s',
                                prev_market_position, market_position)

                if position_qty == 0:
                    raise Exception("[Invalid Order from %s to %s]: Current Position: %s | Qty to Order: %s | Order Action: %s" % (
                        prev_market_position, market_position, str(position_qty), str(qty), trade_side))

                order_data, order_success_message = placeOrder(
                    trd_ctx=trd_ctx, price=price, qty=qty, code=code, trade_side=trade_side, trade_env=trade_env, order_type=order_type, order_time=order_time)

                if order_success_message:
                    success_message = order_success_message
                else:
                    raise Exception("Unable to Place Order: %s" % order_data)

            # From Long/ Short to Opposite
            elif prev_market_position != market_position:
                app.logger.info('Order Buy from %s to %s',
                                prev_market_position, market_position)

                if position_qty == prev_market_position_size:
                    order_data, order_success_message = placeOrder(
                        trd_ctx=trd_ctx, price=price, qty=prev_market_position_size, code=code, trade_side=trade_side, trade_env=trade_env, order_type=order_type, order_time=order_time)
                    time.sleep(0.5)

                order_data, order_success_message = placeOrder(
                    trd_ctx=trd_ctx, price=price, qty=market_position_size, code=code, trade_side=trade_side, trade_env=trade_env, order_type=order_type, order_time=order_time)

                if order_success_message:
                    success_message = order_success_message
                else:
                    raise Exception(
                        "Unable to Place Order: %s" % order_data)

            # Send TG Success Message
            success_message = "Order Place: %s\nCurrent Position: %s %s" % (
                success_message, market_position, data['strategy']['position_size'])
            app.logger.info(success_message)
            if bot:
                bot.send_message(text=success_message,
                                 chat_id=telegram_chat_id)
        except Exception as e:
            message = json.dumps({
                "code": "error",
                "message": json.loads(request.data),
                "error": str(e)
            })
            app.logger.error('ERROR: %s', message)

            if bot:
                bot.send_message(text=message, chat_id=telegram_chat_id)
        finally:
            if trd_ctx:
                trd_ctx.close()
    else:
        tg_message = f"{data['title']}:\n{data['exchange']}-{data['ticker']} {data['strategy']['order_action']} {data['strategy']['order_price']}@{data['strategy']['order_contracts']} \nCurrent Position Size: {data['strategy']['position_size']}"
        if bot:
            bot.send_message(text=tg_message, chat_id=telegram_chat_id)

    app.logger.info('END\n==========')

    return message


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    # app.run(debug=True, port=5000)
