from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters
import requests

# 🔑 مفتاح DeepAI API
DEEPAI_API_KEY = "df6d8e18-fd46-4749-8dae-82e489809243"

# دالة البدء
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("📝 اختبار تحديد الميول المهني", callback_data='career_test')],
        [InlineKeyboardButton("📊 حساب المعدل التراكمي", callback_data='gpa_calc')],
        [InlineKeyboardButton("📚 التخصصات الجامعية في السعودية", callback_data='majors')],
        [InlineKeyboardButton("🏫 روابط الجامعات وبوابات القبول", callback_data='universities')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("مرحبًا بك في بوت Universitytracksa_bot! اختر أحد الخيارات التالية:", reply_markup=reply_markup)

# دالة اختبار الميول المهني باستخدام DeepAI
async def career_test(update: Update, context: CallbackContext) -> None:
    await update.callback_query.message.reply_text("مرحبًا! سأقوم بمساعدتك في تحديد ميولك المهنية. أخبرني عن اهتماماتك وخبراتك.")

    # بدء محادثة مع DeepAI
    context.user_data['chat_history'] = []
    await ask_deepai(update, context, "أخبرني عن اهتماماتك وخبراتك.")

# دالة التفاعل مع DeepAI
async def ask_deepai(update: Update, context: CallbackContext, user_input: str) -> None:
    # إرسال الرسائل إلى DeepAI
    response = requests.post(
        "https://api.deepai.org/api/chatbot",
        data={
            "text": user_input
        },
        headers={
            "api-key": DEEPAI_API_KEY
        }
    )

    # الحصول على رد DeepAI
    if response.status_code == 200:
        deepai_reply = response.json()['output']
    else:
        deepai_reply = "عذرًا، حدث خطأ أثناء معالجة طلبك. يرجى المحاولة مرة أخرى."

    # إرسال رد DeepAI إلى المستخدم
    await update.callback_query.message.reply_text(deepai_reply)

# دالة معالجة الرسائل النصية
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    if 'chat_history' in context.user_data:
        await ask_deepai(update, context, user_input)

# دالة حساب المعدل التراكمي
async def gpa_calc(update: Update, context: CallbackContext) -> None:
    await update.callback_query.message.reply_text("حساب المعدل التراكمي: أدخل درجاتك لحساب المعدل.")

# دالة عرض التخصصات الجامعية
async def majors(update: Update, context: CallbackContext) -> None:
    await update.callback_query.message.reply_text("📚 التخصصات الجامعية في السعودية: طب، هندسة، علوم الحاسب، إدارة الأعمال، وغيرها.")

# دالة عرض روابط الجامعات
async def universities(update: Update, context: CallbackContext) -> None:
    await update.callback_query.message.reply_text("🏫 روابط الجامعات وبوابات القبول في السعودية:")
    links = "\n".join([
        "جامعة الملك سعود: https://ksu.edu.sa",
        "جامعة الملك عبدالعزيز: https://kau.edu.sa",
        "جامعة الملك فهد للبترول والمعادن: https://kfupm.edu.sa"
    ])
    await update.callback_query.message.reply_text(links)

# دالة معالجة الأزرار
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == 'career_test':
        await career_test(update, context)
    elif query.data == 'gpa_calc':
        await gpa_calc(update, context)
    elif query.data == 'majors':
        await majors(update, context)
    elif query.data == 'universities':
        await universities(update, context)
    elif query.data == 'start':
        await start(update, context)

# دالة التشغيل الرئيسية
def main():
    # استبدل التوكن هنا
    TOKEN = "8188434429:AAH9B-GEwvFeX1jAO-IEraQShr9ZKjV-d7g"
    application = Application.builder().token(TOKEN).build()

    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # بدء البوت
    application.run_polling()

if __name__ == '__main__':
    main()
