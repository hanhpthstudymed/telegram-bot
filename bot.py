from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("TOKEN")

balance = 0


# format tiền: 25000000 -> 25.000.000
def format_money(x):
    return format(int(x), ",").replace(",", ".")


# chuyển "590.000" -> 590000
def parse_money(text):
    return float(text.replace(".", "").replace(",", "").strip())


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global balance
    text = update.message.text.strip()

    try:
        # 👉 chỉ lấy dòng đầu tiên
        first_line = text.split("\n")[0].strip()

        # ➕ cộng tiền
        if first_line.startswith("+"):
            amount_str = first_line.replace("+", "").strip()
            amount = parse_money(amount_str)

            balance += amount
            await update.message.reply_text(
                f"➕ +{format_money(amount)}\n💰 Số dư: {format_money(balance)}"
            )

        # ➖ trừ tiền
        elif first_line.startswith("-"):
            amount_str = first_line.replace("-", "").strip()
            amount = parse_money(amount_str)

            balance -= amount
            await update.message.reply_text(
                f"➖ -{format_money(amount)}\n💰 Số dư: {format_money(balance)}"
            )

        # 🔄 reset số dư
        elif first_line.startswith("#dcsd"):
            parts = first_line.split()
            if len(parts) == 2:
                balance = parse_money(parts[1])
                await update.message.reply_text(
                    f"🔄 Reset số dư: {format_money(balance)}"
                )
            else:
                await update.message.reply_text("❌ Dùng đúng: #dcsd 100")

        else:
            await update.message.reply_text(
                "❓ Cú pháp:\n+ 500000\n- 200000\n#dcsd 100000"
            )

    except:
        await update.message.reply_text("❌ Sai định dạng tiền")


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("🤖 Bot đang chạy...")
app.run_polling()