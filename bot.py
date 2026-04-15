from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# số dư (tạm thời - sẽ mất khi tắt bot)
balance = 0


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global balance
    text = update.message.text.strip()

    try:
        # cộng tiền
        if text.startswith("+"):
            amount = float(text.replace("+", "").strip())
            balance += amount
            await update.message.reply_text(f"➕ +{amount}\n💰 Số dư: {balance}")

        # trừ tiền
        elif text.startswith("-"):
            amount = float(text.replace("-", "").strip())
            balance -= amount
            await update.message.reply_text(f"➖ -{amount}\n💰 Số dư: {balance}")

        # reset số dư
        elif text.startswith("#dcsd"):
            parts = text.split()
            if len(parts) == 2:
                balance = float(parts[1])
                await update.message.reply_text(f"🔄 Reset số dư: {balance}")
            else:
                await update.message.reply_text("❌ Sai cú pháp. Dùng: #dcsd 100")

        else:
            await update.message.reply_text("❓ Cú pháp:\n+50\n-20\n#dcsd 100")

    except ValueError:
        await update.message.reply_text("❌ Số tiền không hợp lệ")


# 🔑 DÁN TOKEN CỦA BẠN VÀO ĐÂY
TOKEN = "8503547183:AAHtm7F6b71dE6LxH-gn4XHUK-ZERDJrpN0"

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("🤖 Bot đang chạy...")
app.run_polling()