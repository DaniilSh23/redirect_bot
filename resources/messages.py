"""
Тут тексты сообщений под разные языки интерфейса
"""

MESSAGES = {
    "START_HANDLER_MESSAGE_rus": (
        "🤝Здравствуйте.\n🎁Этот бот поможет <b>обернуть Ваши ссылки</b> для редиректа.\n\n"
        "🪙<b>Стоимость</b> одного редиректа для ссылки: <b>{tariff_response} RUB.</b>\n\n"
        "Нажимайте на кнопку <b>🔗СОЗДАТЬ ССЫЛКУ</b> и приступим."
    ),
    "START_HANDLER_MESSAGE_eng": (
        "🤝Hello.\n🎁This bot will help to wrap your links for redirect.\n\n"
        "🪙The cost of one redirect for a link: {tariff_response} RUB.\n\n"
        "Click on the button 🔗 Create Link and let's get started."
    ),
    "send_link_id_rus": "📊Пришлите <b>ID ссылки</b> для проверки статистики.",
    "send_link_id_eng": "📊Send a <b>link ID</b> to check the stats.",
    "faq_instruction_rus": f"‼️ Обязательно к прочтению.\n\n"
    f"1️⃣ 1 редирект ссылка выдерживает до 3000 сообщение (исключения бывают ввиде 5000-6000 "
    f"сообщений,"
    f"но это большой риск, что из-за ссылки на таком объёме Вы можете убить аккаунты "
    f"(может быть много жалоб на 1 ссылку)\n\n"
    f"2️⃣ Оптимальный объём на 1 редирект ссылку (по личному опыту) составляет 1500-2000 "
    f"сообщений \n\n"
    f"3️⃣ Если на редирект ссылку начинают активно кидать жалобы во врема рассылки, она может "
    f"уйти в спамблок"
    f"(как это проверить? - аккаунты сразу ловят спамблок или бан при попытке разослать эту "
    f"ссылку)."
    f"Это может произойти раньше чем Вы отправите, например 2000 сообщений. "
    f"В этом случае стоит заменить ссылку (сделать новую) или использовать другую "
    f"(если Вы заказали несколько ссылок)\n\n"
    f"4️⃣На 1 источник Вы можете сделать бесконечное количество редирект "
    f"ссылок и каждая ссылку будет уникальна для Телеграм.\n\n"
    f"5️⃣ Перед тем как заказать несколько ссылок, попробуйте сначала заказать 1 "
    f"(во избежание недопониманий)\n\n"
    f"6️⃣ Сокращатели ссылок тоже важная вещь - Вы можете попробовать разные сокращатели и "
    f"выбрать под себя"
    f"оптимальный. Разницы особо нет, но бывает такое что какой то сокращатель не нравится "
    f"телеграму в этот"
    f"самый день и в определенном посте (например, текст + ссылка + картинка), "
    f"в этом случае стоит сменить сокращатель и попробовать другой\n\n"
    f"7️⃣ Прежде чем заказывать большой объём (уже написано в п.5, но я повторюсь) "
    f"закажите 1 ссылку и попробуйте тестово отправить её\n\n"
    f"8️⃣ Если Вы передумали делать редирект, но сумма на Вашем кабинете имеется - возврат "
    f"средств не"
    f"предусмотрен в финансовом эквиваленте, Вы можете потратить их в будущем на редирект "
    f"ссылки\n\n"
    f"9️⃣Если Вы сделали редирект ссылку - но она не рассылается, то в течении 5 часов (после "
    f"создания)"
    f"Вы можете написать в нашу поддержку для замены той самой ссылки (при условии что вы не "
    f"слали"
    f"её более чем 10+ сообщений. Мы проверим по системе и если рассылки как таковой не было с "
    f"этой"
    f"ссылки - мы заменим Вам её или вернем сумму на баланс",
    "faq_instruction_eng": "‼️ A must read.️\n\n1) 1 redirect link withstands up to 3000 messages (exceptions are in the "
    "form of 5000-6000 messages, but it is a big risk that because of the link on this volume "
    "you can kill accounts (there may be many complaints about 1 link).\n\n"
    "2)️ Optimal volume for 1 redirect link (from personal experience) is 1500-2000 messages.\n\n"
    "3)️ If the redirect link gets a lot of complaints during the mailing, it may go into "
    "spamblock (how to check it? - Accounts immediately get spamblocked or banned when trying "
    "to send out this link). This may happen before you send, for example, 2000 messages. "
    "In this case you should replace the link (make a new one) or use another one "
    "(if you ordered several links).\n\n"
    "4)️ On 1 source you can make an infinite number of redirect links and each link will be "
    "unique for Telegram.\n\n"
    "5)️ Before ordering several links, try to order 1 first (to avoid misunderstandings).\n\n"
    "6)️ Link shorteners are also an important thing - you can try different shorteners and "
    "choose the best one for you. There is not much difference, but it happens that some "
    "shortener does not like Telegram on this very day and in a certain post (for example, "
    "text + link + picture), in this case it is worth changing the shortener and try another one\n\n"
    "7)️ Before ordering a large volume (already written in point 5, but I will repeat myself) "
    "order 1 link and try to test send it",
    "support_message_rus": "🆘 Если у Вас имеется вопрос или Вам нужна помощь, напишите нам: {support_username}",
    "support_message_eng": "🆘 If you have a question or need help, email us: : {support_username}",
    "your_balance_rus": "💰<b>Ваш баланс:</b> {balance} RUB",
    "your_balance_eng": "💰<b>Your balance:</b> {balance} RUB",
    "get_transaction_rus": "👌<b>Окей.\nЯ соберу всю Вашу историю операций в один файл и пришлю. Ожидайте...</b>\n\n"
    "💰<b>Ваш баланс:</b> {balance} руб.",
    "get_transaction_eng": "👌Okay.\nI will compile all your transaction history into one file and send it. Wait...\n\n"
    "💰<b>Your balance:</b> {balance} RUB",
    "choose_language_rus": "🗣 Выберите язык интерфейса ",
    "choose_language_eng": "🗣 Select interface language",
    "main_menu_rus": "<b>Главное меню</b>",
    "main_menu_eng": "<b>Main menu</b>",
    "send_file_with_links_rus": f"📄Пожалуйста, пришлите мне <b><u>TXT</u> файл со ссылками</b>:\n\n"
    f"🔹 каждая ссылка с новой строки;\n"
    f"🔹 ссылки должны начинаться с <code>http://</code> <code>https://</code> <code>ftp://"
    f"</code> и т.п.;\n🔹 <b>невалидные ссылки не будут прочитаны.</b>",
    "send_file_with_links_eng": f"📄Please send me a <b><u>TXT</u> file with links</b>:\n\n"
    f"🔹 quick link starting on a new line;\n"
    f"🔹 links must start with <code>http://</code> <code>https://</code> <code>ftp://"
    f"</code>, etc.;\n🔹 <b>invalid links will not be read.</b>",
    "document_processing_rus": f"🖍Обрабатываю Ваш документ.\n\n⏳Это может занять некоторое время, если в документе "
    f"много ссылок.\n<b>Пожалуйста, ожидайте.</b>",
    "document_processing_eng": "🖍Processing your document.\n\n⏳This may take some time if there are many links in "
    "the document.\n<b>Please expect.</b>",
    "file_processing_complete_rus": "✅<b>Обработка файла завершена.</b>\n\n💾<b>Записано: {link_count} "
    "ссылок</b>\n\n💲Цена редиректа для 1 ссылки: <b>{tariff} руб.</b>\n"
    "💰Баланс: <b>{balance} руб.</b>\n"
    "🧾Общая стоимость: <b>{total_price} руб.</b>\n\n"
    "🔀Выберите <b>сколько</b> делать <b>редиректов</b> для каждой ссылки?",
    "file_processing_complete_eng": "✅<b>File processing complete.</b>\n\n💾<b>Recorded: {link_count} "
    "links</b>\n\n💲Redirect price for 1 link: <b>{tariff} RUB</b>\n"
    "💰Balance: <b>{balance} RUB</b>\n"
    "🧾Total cost: <b>{total_price} RUB</b>\n\n"
    "🔀Select <b>how many redirects</b> to make for each link?",
    "choose_shortener_rus": "🔗Пожалуйста, выберите <b>сервис для сокращения ссылок</b>.\n\n"
    "Будьте внимательны! Некоторые сокращалки открывают ссылку спустя n-oe кол-во времени!\n\n"
    "⚜️ Наши домены - мгновенный переход. Улучшенная фильтрация.\n"
    "🔹 сlck.ru - мгновенный переход\n"
    "🔹 kurl.ru - мгновенный переход\n"
    "🔹 haa.su - переход в теч. 3 сек.",
    "choose_shortener_eng": "🔗Please choose a <b>service to shorten links.</b>\n\n"
    "🔗 Be careful! Some abbreviations open the link after a while!\n\n"
    "⚜️ Our domains - instant transfer. Improved filtering.\n🔹 slk.ru - instant transfer\n"
    "🔹 kurl.ru - instant transfer\n🔹 haa.su - jump within 3 sec.",
    "wrap_in_redirect_rus": "🆗Окей.\n🎁Начинаю оборачивать Ваши ссылки в редирект.\n"
    "🧘‍♀️Ожидайте, я пришлю Вам файл с результатами📄, когда всё будет готово.",
    "wrap_in_redirect_eng": "🆗Okay.\n🎁 I will start wrapping your links in redirect.\n"
    "🧘‍♀️Please wait, I'll send you a file with the results📄 when it's done.",
    "make_redirect_status_rus": "☑️<b>Выбрано {redirect_numb} редиректов для каждой ссылки</b>\n\n💾Записано: "
    "<b>{links_count}</b> ссылок\n\n💲Цена редиректа для 1 ссылки: <b>{tariff} руб.</b>\n"
    "💰Баланс: <b>{balance} руб.</b>\n🧾Общая стоимость: <b>{total_price} руб.</b>\n\n"
    "🔀Выберите <b>сколько</b> делать <b>редиректов</b> для каждой ссылки?",
    "make_redirect_status_eng": "☑️<b>{redirect_numb} selected redirects for each link</b>\n\n💾Recorded: "
    "<b>{links_count}</b> links\n\n💲Redirect price for 1 link: <b>{tariff} rub</b>"
    "\n💰Balance: <b>{balance} rub.</b>\n🧾Total cost: <b>{total_price} rub.</b>\n\n"
    "🔀Select <b>how many redirects</b> to make for each link?",
    "less_one_redirect_rus": "❗️<b>Редиректов не может быть меньше 1</b>\n",
    "less_one_redirect_eng": "❗️<b>Redirects cannot be less than 1</b>\n",
    "top_up_balance_for_redirect_rus": "❗️<b>Недостаточно средств, пополните баланс на {price_difference} руб.</b>\n\n",
    "top_up_balance_for_redirect_eng": "❗️<b>Insufficient funds, top up your balance by {price_difference} RUB</b>\n\n",
    "request_stats_rus": "📡Запрашиваю данные о статистике...",
    "request_stats_eng": "📡 Requesting stats...",
    "data_not_received_or_zero_rus": "<i>Данные не получены или 0</i>",
    "data_not_received_or_zero_eng": "<i>Data not received or 0</i>",
    "statistic_info_today_rus": "📆Период статистики: <b>сегодня</b>\n\n🔗<b>ID ссылки:</b> {company_id}\n"
    "🚶<b>Всего переходов:</b> {all_clicks}\n🚶‍♂️<b>Уникальных переходов:</b> "
    "{unique_clicks}\n🤖 <b>Боты:</b> {bots}\n",
    "statistic_info_today_eng": "📆Statistics period: <b>today</b>\n\n🔗<b>Reference ID:</b> {company_id}\n"
    "🚶<b>Total hits:</b> {all_clicks}\n🚶‍♂️<b>Уникальных hits:</b> {unique_clicks}\n"
    "🤖 <b>Bots:</b> {bots}\n",
    "statistic_info_rus": "📆Период статистики: <b>{stat_periods}</b>\n\n🔗<b>ID ссылки:</b> {company_id}\n"
    "🚶<b>Всего переходов:</b> {all_clicks}\n🚶‍♂️<b>Уникальных переходов:</b> "
    "{unique_clicks}\n🤖 <b>Боты:</b> {bots}\n",
    "statistic_info_eng": "📆Statistics period: <b>{stat_periods}</b>\n\n🔗<b>Reference ID:</b> {company_id}\n"
    "🚶<b>Total hits:</b> {all_clicks}\n🚶‍♂️<b>Уникальных hits:</b> {unique_clicks}\n"
    "🤖 <b>Bots:</b> {bots}\n",
}

STAT_PERIODS_RUS = {
    "today": "сегодня",
    "yesterday": "вчера",
    "last_monday": "текущая неделя",
    "7_days_ago": "последние 7 дней",
    "first_day_of_this_month": "текущий месяц",
    "previous_month": "предыдущий месяц",
    "1_month_ago": "последние 30 дней",
    "first_day_of_this_year": "текущий год",
    "1_year_ago": "за год",
    "all_time": "за всё время",
}

STAT_PERIODS_ENG = {
    "today": "today",
    "yesterday": "yesterday",
    "last_monday": "Current week",
    "7_days_ago": "7 days ago",
    "first_day_of_this_month": "Current month",
    "previous_month": "Previous month",
    "1_month_ago": "Last 30 days",
    "first_day_of_this_year": "Current year",
    "1_year_ago": "For the year",
    "all_time": "All time",
}

ERROR_MESSAGES = {
    "base_error_rus": f"🔧<b>Техническая неисправность бота.</b>\nПожалуйста, сообщите нам через раздел поддержки, "
    f"чтобы мы могли оперативно устранить проблему.",
    "base_error_eng": f"🔧<b>Technical malfunction of the bot.</b>\nPlease let us know via the support section so we "
    f"can fix the problem promptly.",
    "translation_error": "🛠 Sorry...The bot has problems with translation. Please try again later, we are already "
    "solving this problem",
}

ALERT_MESSAGES = {
    "return_to_main_rus": "Возврат к главному меню",
    "return_to_main_eng": "Return to the main menu",
    "cancel_and_return_rus": "Нажата кнопка ❌Отменить.\nВозврат к главному меню.",
    "cancel_and_return_eng": "The cancel button is pressed ❌ .\nReturn to the main menu.",
    "send_file_with_links_rus": f"📄Пришлите файл со ссылками:\n\n🔹 каждая ссылка с новой строки;\n"
    f"🔹 все ссылки должны начинаться с http:// https:// ftp:// и т.п.",
    "send_file_with_links_eng": f"📄Send a file of links:\n\n🔹 each link on a new line;\n"
    f"🔹 all links should start with http:// https:// ftp:// etc.",
    "choose_shortener_rus": "🔗Выбор сервиса для сокращения ссылок\n\n🔹 сlck.ru - мгновенный переход\n🔹 kurl.ru - мгновенный переход\n🔹 cleanuri.com - мгновенный переход\n🔹 haa.su - переход в теч. 3 сек.\n",
    "choose_shortener_eng": "🔗Choose a service to shorten links.\n\n🔹 сlck.ru - instant transition\n🔹 kurl.ru - instant transition\n🔹 cleanuri.com - instant transition\n🔹 haa.su - transition within 3 sec.\n",
}
