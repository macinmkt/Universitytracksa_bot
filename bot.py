from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

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

# دالة اختبار الميول المهني
async def career_test(update: Update, context: CallbackContext) -> None:
    questions = [
        ("هل تفضل العمل مع الأرقام؟", ["نعم", "لا"]),
        ("هل تحب العمل الجماعي؟", ["نعم", "لا"]),
        ("هل تستمتع بحل المشكلات التقنية؟", ["نعم", "لا"])
    ]
    context.user_data['career_test'] = questions
    await ask_question(update, context, 0)

# دالة طرح الأسئلة
async def ask_question(update: Update, context: CallbackContext, index: int) -> None:
    if index < len(context.user_data['career_test']):
        question, answers = context.user_data['career_test'][index]
        keyboard = [[InlineKeyboardButton(answer, callback_data=f'q_{index}_{answer}')] for answer in answers]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text(question, reply_markup=reply_markup)
    else:
        await update.callback_query.message.reply_text("تم الانتهاء من الاختبار! سيتم تحليل إجاباتك وإرسال النتيجة لاحقًا.")

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
    elif query.data.startswith('q_'):
        _, index, _ = query.data.split('_')
        await ask_question(update, context, int(index) + 1)
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

    # بدء البوت
    application.run_polling()

if __name__ == '__main__':
    main()
