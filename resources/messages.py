"""
Тут тексты сообщений под разные языки интерфейса
"""

MESSAGES = {
    "START_HANDLER_MESSAGE_rus": ('🤝Здравствуйте.\n🎁Этот бот поможет <b>обернуть Ваши ссылки</b> для редиректа.\n\n'
                                  '🪙<b>Стоимость</b> одного редиректа для ссылки: <b>{tariff_response} RUB.</b>\n\n'
                                  'Нажимайте на кнопку <b>🔗СОЗДАТЬ ССЫЛКУ</b> и приступим.'),
    "START_HANDLER_MESSAGE_eng": ("🤝Hello.\n🎁This bot will help to wrap your links for redirect.\n\n"
                                  "🪙The cost of one redirect for a link: {tariff_response} RUB.\n\n"
                                  "Click on the button 🔗 Create Link and let's get started."),
    "send_link_id_rus": "📊Пришлите <b>ID ссылки</b> для проверки статистики.",
    "send_link_id_eng": "📊Send a <b>link ID</b> to check the stats.",
    "faq_instruction_rus": f'‼️ Обязательно к прочтению.\n\n'
                           f'1️⃣ 1 редирект ссылка выдерживает до 3000 сообщение (исключения бывают ввиде 5000-6000 '
                           f'сообщений,'
                           f'но это большой риск, что из-за ссылки на таком объёме Вы можете убить аккаунты '
                           f'(может быть много жалоб на 1 ссылку)\n\n'
                           f'2️⃣ Оптимальный объём на 1 редирект ссылку (по личному опыту) составляет 1500-2000 '
                           f'сообщений \n\n'
                           f'3️⃣ Если на редирект ссылку начинают активно кидать жалобы во врема рассылки, она может '
                           f'уйти в спамблок'
                           f'(как это проверить? - аккаунты сразу ловят спамблок или бан при попытке разослать эту '
                           f'ссылку).'
                           f'Это может произойти раньше чем Вы отправите, например 2000 сообщений. '
                           f'В этом случае стоит заменить ссылку (сделать новую) или использовать другую '
                           f'(если Вы заказали несколько ссылок)\n\n'
                           f'4️⃣На 1 источник Вы можете сделать бесконечное количество редирект '
                           f'ссылок и каждая ссылку будет уникальна для Телеграм.\n\n'
                           f'5️⃣ Перед тем как заказать несколько ссылок, попробуйте сначала заказать 1 '
                           f'(во избежание недопониманий)\n\n'
                           f'6️⃣ Сокращатели ссылок тоже важная вещь - Вы можете попробовать разные сокращатели и '
                           f'выбрать под себя'
                           f'оптимальный. Разницы особо нет, но бывает такое что какой то сокращатель не нравится '
                           f'телеграму в этот'
                           f'самый день и в определенном посте (например, текст + ссылка + картинка), '
                           f'в этом случае стоит сменить сокращатель и попробовать другой\n\n'
                           f'7️⃣ Прежде чем заказывать большой объём (уже написано в п.5, но я повторюсь) '
                           f'закажите 1 ссылку и попробуйте тестово отправить её\n\n'
                           f'8️⃣ Если Вы передумали делать редирект, но сумма на Вашем кабинете имеется - возврат '
                           f'средств не'
                           f'предусмотрен в финансовом эквиваленте, Вы можете потратить их в будущем на редирект '
                           f'ссылки\n\n'
                           f'9️⃣Если Вы сделали редирект ссылку - но она не рассылается, то в течении 5 часов (после '
                           f'создания)'
                           f'Вы можете написать в нашу поддержку для замены той самой ссылки (при условии что вы не '
                           f'слали'
                           f'её более чем 10+ сообщений. Мы проверим по системе и если рассылки как таковой не было с '
                           f'этой'
                           f'ссылки - мы заменим Вам её или вернем сумму на баланс',
    "faq_instruction_eng": "‼️ A must read.️ 1) 1 redirect link withstands up to 3000 messages (exceptions are in the "
                           "form of 5000-6000 messages, but it is a big risk that because of the link on this volume "
                           "you can kill accounts (there may be many complaints about 1 link).\n "
                           "2)️ Optimal volume for 1 redirect link (from personal experience) is 1500-2000 messages. \n"
                           "3)️ If the redirect link gets a lot of complaints during the mailing, it may go into "
                           "spamblock (how to check it? - Accounts immediately get spamblocked or banned when trying "
                           "to send out this link). This may happen before you send, for example, 2000 messages. "
                           "In this case you should replace the link (make a new one) or use another one "
                           "(if you ordered several links).\n"
                           "4)️ On 1 source you can make an infinite number of redirect links and each link will be "
                           "unique for Telegram.\n"
                           "5)️ Before ordering several links, try to order 1 first (to avoid misunderstandings).\n"
                           "6)️ Link shorteners are also an important thing - you can try different shorteners and "
                           "choose the best one for you. There is not much difference, but it happens that some "
                           "shortener does not like Telegram on this very day and in a certain post (for example, "
                           "text + link + picture), in this case it is worth changing the shortener and try another one\n"
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
    "choose_language_rus": "👅 Выберите язык интерфейса ",
    "choose_language_eng": "👅 Select interface language",
}

ERROR_MESSAGES = {
    "base_error": "🛠 Sorry...The bot has problems. Please try again later, we are already solving this problem!",
    "translation_error": "🛠 Sorry...The bot has problems with translation. Please try again later, we are already "
                         "solving this problem",
}
