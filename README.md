# Tradingview Futu Python Bot Setup

The setup aims to use Tradingview alert function to do trade. There are a lot of tutorial in Youtube for using Internet Brokers but not for Futu. The webhook can detect the trading position through the previous and current trading position from Tradingview message. The position size depends on Tradingview message too. Thus please edit the Python script on your own logic.

# Disclaimer

These strategies are for educational purposes only. Do not risk money which you are afraid to lose. USE THE SOFTWARE AT YOUR OWN RISK. THE AUTHORS AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS.

Always start by testing strategies and setup with a simulate environment first then run the trading bot. Do not engage money before you understand how it works and what profit/loss you should expect.

I strongly recommend you to have coding and Python knowledge. Do not hesitate to read the source code and edit your own logic.

# How to use

Please follow the README of futu-endpoint and then webhook.

# How to test

Send POST request with below JSON content to http://your-domain/webhook
It will place a order from FLAT to LONG.

```
{
  "passphrase": "ioXjHyG8uR",
  "title": "",
  "time": "2022-11-07T22:00:00Z",
  "exchange": "BATS",
  "ticker": "MSFT",
  "bar": {
    "time": "2022-11-07T15:40:00Z",
    "open": "302.38",
    "high": "302.84",
    "low": "302.06",
    "close": "302.43",
    "volume": "29534"
  },
  "strategy": {
    "position_size": "30",
    "order_action": "buy",
    "order_contracts": "14",
    "order_price": "302.43",
    "order_id": "",
    "market_position": "long",
    "market_position_size": "24",
    "prev_market_position": "flat",
    "prev_market_position_size": "0"
  },
  "is_auto": true,
  "market": "US",
  "environment": "SIMULATE",
  "currency": "USD"
}
```
