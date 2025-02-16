from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("📝 اختبار تحديد الميول المهني", callback_data='career_test')],
        [InlineKeyboardButton("📊 حساب المعدل التراكمي", callback_data='gpa_calc')],
        [InlineKeyboardButton("📚 التخصصات الجامعية في السعودية", callback_data='majors')],
        [InlineKeyboardButton("🏫 روابط الجامعات وبوابات القبول", callback_data='universities')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("مرحبًا بك في بوت Universitytracksa_bot! اختر أحد الخيارات التالية:", reply_markup=reply_markup)

def career_test(update: Update, context: CallbackContext) -> None:
    questions = [
        ("هل تفضل العمل مع الأرقام؟", ["نعم", "لا"]),
        ("هل تحب العمل الجماعي؟", ["نعم", "لا"]),
        ("هل تستمتع بحل المشكلات التقنية؟", ["نعم", "لا"])
    ]
    context.user_data['career_test'] = questions
    ask_question(update, context, 0)

def ask_question(update: Update, context: CallbackContext, index: int) -> None:
    if index < len(context.user_data['career_test']):
        question, answers = context.user_data['career_test'][index]
        keyboard = [[InlineKeyboardButton(answer, callback_data=f'q_{index}_{answer}')] for answer in answers]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text(question, reply_markup=reply_markup)
    else:
        update.callback_query.message.reply_text("تم الانتهاء من الاختبار! سيتم تحليل إجاباتك وإرسال النتيجة لاحقًا.")

def gpa_calc(update: Update, context: CallbackContext) -> None:
    update.callback_query.message.reply_text("حساب المعدل التراكمي: أدخل درجاتك لحساب المعدل.")

def majors(update: Update, context: CallbackContext) -> None:
    update.callback_query.message.reply_text("📚 التخصصات الجامعية في السعودية: طب، هندسة، علوم الحاسب، إدارة الأعمال، وغيرها.")

def universities(update: Update, context: CallbackContext) -> None:
    update.callback_query.message.reply_text("🏫 روابط الجامعات وبوابات القبول في السعودية:")
    links = "\n".join([
        "جامعة الملك سعود: https://ksu.edu.sa",
        "جامعة الملك عبدالعزيز: https://kau.edu.sa",
        "جامعة الملك فهد للبترول والمعادن: https://kfupm.edu.sa"
    ])
    update.callback_query.message.reply_text(links)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'career_test':
        career_test(update, context)
    elif query.data.startswith('q_'):
        _, index, _ = query.data.split('_')
        ask_question(update, context, int(index) + 1)
    elif query.data == 'gpa_calc':
        gpa_calc(update, context)
    elif query.data == 'majors':
        majors(update, context)
    elif query.data == 'universities':
        universities(update, context)
    elif query.data == 'start':
        start(update, context)

def main():
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
