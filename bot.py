from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("TOKEN")

balance = 0


def format_money(x):
    return format(int(x), ",").replace(",", ".")


def parse_money(text):
    return float(text.replace(".", "").replace(",", "").strip())


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global balance

    # 👉 lấy text hoặc caption
    text = ""
    if update.message.text:
        text = update.message.text.strip()
    elif update.message.caption:
        text = update.message.caption.strip()
    else:
        return

    try:
        # 👉 chỉ lấy dòng đầu
        first_line = text.split("\n")[0].strip()

        # ➕ cộng
        if first_line.startswith("+"):
            amount = parse_money(first_line.replace("+", "").strip())
            balance += amount
            await update.message.reply_text(
                f"➕ +{format_money(amount)}\n💰 Số dư: {format_money(balance)}"
            )

        # ➖ trừ
        elif first_line.startswith("-"):
            amount = parse_money(first_line.replace("-", "").strip())
            balance -= amount
            await update.message.reply_text(
                f"➖ -{format_money(amount)}\n💰 Số dư: {format_money(balance)}"
            )

        # 🔄 reset
        elif first_line.startswith("#dcsd"):
            parts = first_line.split()
            if len(parts) == 2:
                balance = parse_money(parts[1])
                await update.message.reply_text(
                    f"🔄 Reset số dư: {format_money(balance)}"
                )
            else:
                await update.message.reply_text("❌ Dùng đúng: #dcsd 100")

    except:
        await update.message.reply_text("❌ Sai định dạng tiền")


app = ApplicationBuilder().token(TOKEN).build()

# 👉 nhận cả text + ảnh + caption
app.add_handler(MessageHandler(filters.ALL, handle))

print("🤖 Bot đang chạy...")
app.run_polling()