# Tradingview Webhook Endpoint

The webhook allows using alert function from Tradingview pine script to call trading actions. This will detect the trade option by comparing previous and current trading position to make LONG/ SHORT/ FLAT side. In addition, this bot allow telegram messaging.

## How to use

1. Copy everything in "request.json" to Tradingview alert message. But remember to config below values.

```
- passphrase: Generate your own passphrase
- is_auto: Deciding to trade with bot or just telegram messaging. If true, the bot will trade. If false, the bot will only alert telegram message [true | false]
- market: The market you trade. ["US" | "HK"]
- environment: The environment you trade at. Please try SIMULATE environment first. ["SIMULATE" | "REAL"]
- currency: The currency your script settled. Recommended USD ["USD | HKD"]
```

2. Build the container and run.

```
$ docker build -t py-futu-webhook .

$ docker run -d -t -i -e TRADING_PWD='YOUR_FUTU_SIX_DIGITS_TRADE_PASSWORD' -e OPEN_D_PEM='PEM_GEN_IN_OPEND' -e OPEN_D_HOST='127.0.0.1' -e OPEN_D_PORT='11111' -e TELEGRAM_TOKEN='TG_TOKEN' -e TELEGRAM_CHAT_ID='TG_CHAT_ID' -e WEBHOOK_PASSPHRASE='YOUR_PASSPHRASE_FROM_MSG' -p 5000:5000 --name py-futu-webhook py-futu-webhook

<!-- Example -->
docker run -d -t -i -e TRADING_PWD='123456' -e OPEN_D_PEM='-----BEGIN RSA PRIVATE KEY-----
MIICWwIBAAKBgG1MN+vxtCbF8bCZlAc8DbxoLNmIYvfC0m6G5hRiPxaRiOZgaw2T
b7F2JRps1OUikAalVK8nm0K/PO0j3uRW2/hdwqPaq0M5jBG8L9hn5aKrfDEVC0Iu
15EUjTrMeTYlXW8Xvx2LZmu4BiVsJdePhtD17hNE9DN0ihNGIadTAUa1AgMBAAEC
gYBc1zJlXFHP4bJ0dXA1WQC9+qumOGEA3l+LfVExHWdDj2n/bwVgac2lq5rGwI1y
+ZHn40Z05irPXsytDxxFT7bXOZUraRRYXkTlGPV34clDuYEku0Ay4S29rUdW+drj
5CoDoKk8iaGWd8VbNdXSDgX1x9Akf0+CTpujDe/JtEzUQQJBAMMrfziFzZW2Sjfa
NM3hi7ULsa00LPNcNDhxVnW3J6+YWd6rplTRuI4FR6rr6lvQYHvdFKqYraWTiA2U
Ocmr0FECQQCPXQahg0mZ0pv20/7smzh80hQ/PBmZa1/AkojvoClK7M+t/w5ev8d4
SnnsNZcwuTaWAgUhgrfo5kQsojJksbslAkASObWfqZ8RI/y6Sn4z26QYPAdTjVPF
Rg76Vlskkv35v9hkmtLliNAbMxMGOxGfkU3xQyvy4l8U3zoNSpI66viBAkBvaihh
FRr6BIdZB+AyGV+JAeriSd7LMHs1uavaLmpo5ClyW6nbUMfAYIDoZa2eHBKj+eXq
6R/sTCfnWBY50zZRAkEAu5Bt8UjxTldfOXnM8ndURtp6wulNAfDD769MIPDulnrn
zdYTS4Kcq7InhpbHur204QzwpvJIXgE2Z30xmL+LWQ==
-----END RSA PRIVATE KEY-----' -e OPEN_D_HOST='127.0.0.1' -e OPEN_D_PORT='11111' -e TELEGRAM_TOKEN='' -e TELEGRAM_CHAT_ID='' -e WEBHOOK_PASSPHRASE='abcdefg' -p 5000:5000 --name py-futu-webhook py-futu-webhook
```

3. In tradingview, set the message alerted by webhook. Copy your url (IP/your own domain) to it.

- Example: http://your-domain/webhook
