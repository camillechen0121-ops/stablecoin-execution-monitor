import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# =========================
# CONFIG
# =========================
TELEGRAM_BOT_TOKEN = "xxx" #Telegram bot token is masked ("xxx") for security reasons.

# =========================
# DATA
# =========================
def get_kraken_usdt_usd():
    url = "https://api.kraken.com/0/public/Ticker?pair=USDTZUSD"
    return float(requests.get(url).json()["result"]["USDTZUSD"]["c"][0])


def get_bitfinex_usdt_usd():
    try:
        url = "https://api.bitfinex.com/v1/pubticker/ustusd"
        return float(requests.get(url).json()["last_price"])
    except:
        return None


def get_binance_usdc_usdt():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=USDCUSDT"
    return float(requests.get(url).json()["price"])


# =========================
# LOGIC
# =========================
def choose_cex(kraken, bitfinex):
    if bitfinex is None:
        return "KRAKEN", kraken
    return ("KRAKEN", kraken) if kraken >= bitfinex else ("BITFINEX", bitfinex)


def binance_effective_usd(usdc_usdt):
    # USDC ≈ USD
    return 1 / usdc_usdt


def run():
    kraken = get_kraken_usdt_usd()
    bitfinex = get_bitfinex_usdt_usd()
    usdc_usdt = get_binance_usdc_usdt()

    venue, cex_price = choose_cex(kraken, bitfinex)

    binance_usd = binance_effective_usd(usdc_usdt)

    diff = binance_usd - cex_price

    if abs(diff) < 0.0001:
        signal = "NO TRADE"
    elif diff > 0:
        signal = "USE BINANCE ROUTE (better USD received)"
    else:
        signal = "USE CEX ROUTE (better USD received)"

    return {
        "kraken": kraken,
        "bitfinex": bitfinex,
        "venue": venue,
        "cex": cex_price,
	"binance_usdc_usdt": usdc_usdt,
        "binance_usd": binance_usd,
        "diff": diff,
        "signal": signal
    }


# =========================
# COMMAND: /price
# =========================
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    s = run()

    msg = (
        "📊 Cross-Venue Liquidity Conversion Monitor\n\n"
        f"USDT/USD (Kraken): {s['kraken']:.4f}\n"
        f"USDT/USD (Bitfinex): {s['bitfinex'] if s['bitfinex'] is not None else 'N/A'}\n"
        f"Selected CEX: {s['venue']}\n"
        f"CEX USD value: {s['cex']:.4f}\n\n"
        f"Binance USDC/USDT: {s['binance_usdc_usdt']:.4f}\n"
        f"Binance effective USD: {s['binance_usd']:.4f}\n\n"
        f"Difference: {s['diff']:.5f}\n\n"
        f"Decision: {s['signal']}"
    )

    await update.message.reply_text(msg)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Liquidity routing monitor running.")


# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
