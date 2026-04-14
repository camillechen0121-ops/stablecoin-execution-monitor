import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# =========================
# CONFIG
# =========================
TELEGRAM_BOT_TOKEN = "xxx" # Telegram bot token is masked ("xxx") for security reasons.

# Fees (maker assumption)
KRAKEN_MAKER_FEE = 0.0
KRAKEN_TAKER_FEE = 0.0001  # not used in maker mode
BINANCE_FEE = 0.0
BITFINEX_WITHDRAWAL_FEE = 0.0002

THRESHOLD_BUFFER = 0.0001  # safety buffer


# =========================
# DATA
# =========================
def get_kraken_usdt_usd():
    url = "https://api.kraken.com/0/public/Ticker?pair=USDTZUSD"
    res = requests.get(url, timeout=5).json()
    return float(res["result"]["USDTZUSD"]["c"][0])


def get_bitfinex_usdt_usd():
    try:
        url = "https://api.bitfinex.com/v1/pubticker/ustusd"
        res = requests.get(url, timeout=5).json()
        return float(res["last_price"])
    except:
        return None


def get_binance_usdc_usdt():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=USDCUSDT"
    res = requests.get(url, timeout=5).json()
    return float(res["price"])


# =========================
# EXECUTION LOGIC
# =========================
def choose_usdt_usd_venue(kraken, bitfinex):
    """
    Maker assumption: choose better quote (no fee impact)
    """

    if bitfinex is None:
        return "KRAKEN", kraken

    if kraken <= bitfinex:
        return "KRAKEN", kraken
    else:
        return "BITFINEX", bitfinex


def compute_usdt_usd_from_binance(usdc_usdt):
    """
    USDT/USD via Binance path
    """
    return 1 / usdc_usdt


def compute_threshold():
    """
    Maker mode → near zero cost
    only buffer + optional withdrawal
    """
    return BITFINEX_WITHDRAWAL_FEE + THRESHOLD_BUFFER


def generate_signal(spread, threshold):
    if abs(spread) < threshold:
        return "NO TRADE"

    if spread > 0:
        return "SELL USDT (CEX overpriced) / BUY via Binance"
    else:
        return "BUY USDT (CEX underpriced) / SELL via Binance"


def run_system():
    kraken = get_kraken_usdt_usd()
    bitfinex = get_bitfinex_usdt_usd()
    usdc_usdt = get_binance_usdc_usdt()

    # 1. venue
    venue, usdt_usd_cex = choose_usdt_usd_venue(kraken, bitfinex)

    # 2. implied
    usdt_usd_binance = compute_usdt_usd_from_binance(usdc_usdt)

    # 3. spread
    spread = usdt_usd_cex - usdt_usd_binance

    # 4. threshold
    threshold = compute_threshold()

    # 5. signal
    signal = generate_signal(spread, threshold)

    return {
        "venue": venue,
        "kraken": kraken,
        "bitfinex": bitfinex,
        "usdt_usd_cex": usdt_usd_cex,
        "usdt_usd_binance": usdt_usd_binance,
        "spread": spread,
        "threshold": threshold,
        "signal": signal
    }


# =========================
# TELEGRAM
# =========================
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        s = run_system()

        msg = (
            "📊 Maker Execution Monitor\n\n"
            f"Venue: {s['venue']}\n"
            f"Kraken: {s['kraken']:.6f}\n"
            f"Bitfinex: {s['bitfinex']}\n\n"
            f"CEX USDT/USD: {s['usdt_usd_cex']:.6f}\n"
            f"Binance Implied: {s['usdt_usd_binance']:.6f}\n\n"
            f"Spread: {s['spread']:.6f}\n"
            f"Threshold: {s['threshold']:.6f}\n\n"
            f"Signal: {s['signal']}"
        )

        await update.message.reply_text(msg)

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Maker-based execution monitor running.")


def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))

    app.run_polling()


if __name__ == "__main__":
    main()
