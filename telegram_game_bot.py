"""
🎮 بات سرگرمی تلگرام
بازی‌های موجود:
  - عدد بخون (حدس عدد)
  - سنگ، کاغذ، قیچی
  - تاس بنداز
  - جوک تصادفی
"""

import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ───────────── تنظیمات ─────────────
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"   # ← توکن بات را اینجا بذار

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ───────────── جوک‌ها ─────────────
JOKES = [
    "چرا برنامه‌نویس‌ها عینک می‌زنن؟ چون نمی‌تونن C# بدون عینک بخونن! 😄",
    "استاد: پسرم درس بخون، آینده‌ات تاریکه!\nدانشجو: پس باید بشم برنامه‌نویس، همیشه با Dark Mode کار می‌کنم! 😂",
    "یه بار یه باگ داشتم که ۳ روز پیداش کردم... معلوم شد نقطه‌ویرگول جا انداختم 😅",
    "بهترین چیز توی زندگی برنامه‌نویسا: Ctrl+Z 😎",
    "مرد: دکتر، هر وقت قهوه می‌خورم چشمم می‌زنه!\nدکتر: قاشوقشو از توش دربیار! ☕",
    "پسر به باباش گفت: بابا الکتریسیته چیه؟\nبابا: برو از مامانت بپرس، اون همه چیزو می‌دونه!\nپسر: پس جریان از اون طرف میاد؟ ⚡",
]

# ───────────── منوی اصلی ─────────────
def main_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🎲 تاس بنداز", callback_data="dice"),
            InlineKeyboardButton("✂️ سنگ کاغذ قیچی", callback_data="rps_menu"),
        ],
        [
            InlineKeyboardButton("🔢 حدس عدد", callback_data="guess_start"),
            InlineKeyboardButton("😂 جوک", callback_data="joke"),
        ],
        [
            InlineKeyboardButton("🏆 امتیاز من", callback_data="score"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# ───────────── /start ─────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # مقداردهی اولیه امتیاز
    if "score" not in context.user_data:
        context.user_data["score"] = 0

    await update.message.reply_text(
        f"سلام {user.first_name}! 👋\n\n"
        "🎮 به بات سرگرمی خوش اومدی!\n"
        "یه بازی انتخاب کن:",
        reply_markup=main_menu_keyboard(),
    )


# ───────────── /menu ─────────────
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 منوی بازی‌ها:",
        reply_markup=main_menu_keyboard(),
    )


# ───────────── پردازش دکمه‌ها ─────────────
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ── تاس ──
    if data == "dice":
        result = random.randint(1, 6)
        faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
        await query.edit_message_text(
            f"🎲 تاس انداختی!\n\n{faces[result - 1]}  عدد {result} اومد!\n\nدوباره بزن:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎲 دوباره", callback_data="dice")],
                [InlineKeyboardButton("🔙 منو", callback_data="back")],
            ]),
        )

    # ── جوک ──
    elif data == "joke":
        joke = random.choice(JOKES)
        await query.edit_message_text(
            f"😂 جوک:\n\n{joke}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("😂 جوک دیگه", callback_data="joke")],
                [InlineKeyboardButton("🔙 منو", callback_data="back")],
            ]),
        )

    # ── سنگ کاغذ قیچی - منو ──
    elif data == "rps_menu":
        keyboard = [
            [
                InlineKeyboardButton("🪨 سنگ", callback_data="rps_rock"),
                InlineKeyboardButton("📄 کاغذ", callback_data="rps_paper"),
                InlineKeyboardButton("✂️ قیچی", callback_data="rps_scissors"),
            ],
            [InlineKeyboardButton("🔙 منو", callback_data="back")],
        ]
        await query.edit_message_text(
            "✂️ سنگ، کاغذ، قیچی!\n\nانتخابت چیه؟",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # ── سنگ کاغذ قیچی - نتیجه ──
    elif data.startswith("rps_"):
        choices = {"rock": "🪨 سنگ", "paper": "📄 کاغذ", "scissors": "✂️ قیچی"}
        wins = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
        user_choice = data.replace("rps_", "")
        bot_choice = random.choice(list(choices.keys()))

        if user_choice == bot_choice:
            result_text = "🤝 مساوی شد!"
        elif wins[user_choice] == bot_choice:
            result_text = "🎉 تو بردی! +10 امتیاز"
            context.user_data["score"] = context.user_data.get("score", 0) + 10
        else:
            result_text = "😅 من بردم!"

        await query.edit_message_text(
            f"تو: {choices[user_choice]}\n"
            f"من: {choices[bot_choice]}\n\n"
            f"{result_text}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 دوباره", callback_data="rps_menu")],
                [InlineKeyboardButton("🔙 منو", callback_data="back")],
            ]),
        )

    # ── حدس عدد - شروع ──
    elif data == "guess_start":
        secret = random.randint(1, 100)
        context.user_data["secret"] = secret
        context.user_data["guess_attempts"] = 0
        await query.edit_message_text(
            "🔢 یه عدد بین ۱ تا ۱۰۰ فکر کردم!\n\n"
            "حدست رو بنویس:",
        )

    # ── امتیاز ──
    elif data == "score":
        score = context.user_data.get("score", 0)
        await query.edit_message_text(
            f"🏆 امتیاز تو: {score} امتیاز\n\n"
            "هر بار که سنگ‌کاغذ‌قیچی ببری +۱۰ امتیاز می‌گیری!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 منو", callback_data="back")],
            ]),
        )

    # ── بازگشت به منو ──
    elif data == "back":
        await query.edit_message_text(
            "🎮 منوی بازی‌ها:",
            reply_markup=main_menu_keyboard(),
        )


# ───────────── پیام‌های متنی (حدس عدد) ─────────────
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # اگر بازی حدس عدد فعاله
    if "secret" in context.user_data:
        secret = context.user_data["secret"]
        try:
            guess = int(update.message.text.strip())
        except ValueError:
            await update.message.reply_text("⚠️ لطفاً یه عدد بفرست!")
            return

        context.user_data["guess_attempts"] += 1
        attempts = context.user_data["guess_attempts"]

        if guess < secret:
            await update.message.reply_text(f"📈 بزرگ‌تره! (تلاش {attempts})")
        elif guess > secret:
            await update.message.reply_text(f"📉 کوچیک‌تره! (تلاش {attempts})")
        else:
            bonus = max(0, 50 - attempts * 5)
            context.user_data["score"] = context.user_data.get("score", 0) + bonus
            del context.user_data["secret"]
            await update.message.reply_text(
                f"🎉 آفرین! عدد {secret} بود!\n"
                f"در {attempts} تلاش پیداش کردی.\n"
                f"{'+ ' + str(bonus) + ' امتیاز!' if bonus > 0 else ''}",
                reply_markup=main_menu_keyboard(),
            )
    else:
        await update.message.reply_text(
            "از منو یه بازی انتخاب کن 👇",
            reply_markup=main_menu_keyboard(),
        )


# ───────────── اجرا ─────────────
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("🤖 بات در حال اجراست...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
