"""
Small hand-rolled i18n layer. Not trying to be a full framework -- just a
dict of strings per language and a t() helper to fetch + format them,
falling back to English if a key or language is missing.
"""

LANGUAGES = [
    ("en", "\U0001F1EC\U0001F1E7 English"),
    ("ru", "\U0001F1F7\U0001F1FA \u0420\u0443\u0441\u0441\u043A\u0438\u0439"),
    ("uz", "\U0001F1FA\U0001F1FF O\u02bbzbekcha"),
]

TRANSLATIONS = {
    "en": {
        "choose_language": "\U0001F310 Choose your language:",
        "welcome": (
            "Hey! I'm a games bot.\n\n"
            "Type my username (@{username}) in <b>any</b> chat \u2014 even a DM with a "
            "friend \u2014 to start a game of tic-tac-toe, vs them or vs an "
            "unbeatable bot.\n\n"
            "Change your language anytime with /language."
        ),
        "waiting": "Waiting for someone else in this chat to tap a square and join as O.",
        "turn": "{symbol} {name}'s turn",
        "draw": "\U0001F91D It's a draw! Tap Rematch to play again.",
        "win": "\U0001F3C6 {name} wins! Tap Rematch to play again.",
        "rematch_button": "\U0001F504 Rematch",
    },
    "ru": {
        "choose_language": "\U0001F310 \u0412\u044B\u0431\u0435\u0440\u0438\u0442\u0435 \u044F\u0437\u044B\u043A:",
        "welcome": (
            "\u041F\u0440\u0438\u0432\u0435\u0442! \u042F \u0431\u043E\u0442 \u0434\u043B\u044F \u0438\u0433\u0440.\n\n"
            "\u041D\u0430\u043F\u0438\u0448\u0438\u0442\u0435 \u043C\u043E\u0439 \u044E\u0437\u0435\u0440\u043D\u0435\u0439\u043C (@{username}) \u0432 <b>\u043B\u044E\u0431\u043E\u043C</b> "
            "\u0447\u0430\u0442\u0435 \u2014 \u0434\u0430\u0436\u0435 \u0432 \u043B\u0438\u0447\u043A\u0435 \u0441 \u0434\u0440\u0443\u0433\u043E\u043C \u2014 \u0447\u0442\u043E\u0431\u044B \u043D\u0430\u0447\u0430\u0442\u044C \u0438\u0433\u0440\u0443 "
            "\u0432 \u043A\u0440\u0435\u0441\u0442\u0438\u043A\u0438-\u043D\u043E\u043B\u0438\u043A\u0438, \u043F\u0440\u043E\u0442\u0438\u0432 \u043D\u0435\u0433\u043E \u0438\u043B\u0438 \u043F\u0440\u043E\u0442\u0438\u0432 \u043D\u0435\u043F\u043E\u0431\u0435\u0434\u0438\u043C\u043E\u0433\u043E "
            "\u0431\u043E\u0442\u0430.\n\n"
            "\u042F\u0437\u044B\u043A \u043C\u043E\u0436\u043D\u043E \u0441\u043C\u0435\u043D\u0438\u0442\u044C \u0432 \u043B\u044E\u0431\u043E\u0439 \u043C\u043E\u043C\u0435\u043D\u0442 \u043A\u043E\u043C\u0430\u043D\u0434\u043E\u0439 /language."
        ),
        "waiting": "\u0416\u0434\u0451\u043C, \u043F\u043E\u043A\u0430 \u043A\u0442\u043E-\u0442\u043E \u0435\u0449\u0451 \u0432 \u044D\u0442\u043E\u043C \u0447\u0430\u0442\u0435 \u043D\u0430\u0436\u043C\u0451\u0442 \u043D\u0430 \u043A\u043B\u0435\u0442\u043A\u0443 \u0438 \u0441\u0442\u0430\u043D\u0435\u0442 O.",
        "turn": "{symbol} \u0425\u043E\u0434 \u0438\u0433\u0440\u043E\u043A\u0430 {name}",
        "draw": "\U0001F91D \u041D\u0438\u0447\u044C\u044F! \u041D\u0430\u0436\u043C\u0438\u0442\u0435 \u00AB\u0420\u0435\u0432\u0430\u043D\u0448\u00BB, \u0447\u0442\u043E\u0431\u044B \u0441\u044B\u0433\u0440\u0430\u0442\u044C \u0435\u0449\u0451 \u0440\u0430\u0437.",
        "win": "\U0001F3C6 {name} \u043F\u043E\u0431\u0435\u0436\u0434\u0430\u0435\u0442! \u041D\u0430\u0436\u043C\u0438\u0442\u0435 \u00AB\u0420\u0435\u0432\u0430\u043D\u0448\u00BB, \u0447\u0442\u043E\u0431\u044B \u0441\u044B\u0433\u0440\u0430\u0442\u044C \u0435\u0449\u0451 \u0440\u0430\u0437.",
        "rematch_button": "\U0001F504 \u0420\u0435\u0432\u0430\u043D\u0448",
    },
    "uz": {
        "choose_language": "\U0001F310 Tilni tanlang:",
        "welcome": (
            "Salom! Men o'yinlar boti man.\n\n"
            "<b>Har qanday</b> chatda \u2014 hatto do'stingiz bilan shaxsiy yozishmada ham \u2014 "
            "mening usernamemni (@{username}) yozing va krestik-nolik o'yinini boshlang, "
            "do'stingizga yoki yengilmas botga qarshi.\n\n"
            "Tilni istalgan vaqtda /language buyrug'i bilan almashtirishingiz mumkin."
        ),
        "waiting": "Ushbu chatdagi boshqa birov katakchani bosib, O sifatida qo'shilishini kutyapmiz.",
        "turn": "{symbol} {name} navbati",
        "draw": "\U0001F91D Durrang! Qayta o'ynash uchun Rematch tugmasini bosing.",
        "win": "\U0001F3C6 {name} yutdi! Qayta o'ynash uchun Rematch tugmasini bosing.",
        "rematch_button": "\U0001F504 Qayta o'ynash",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    strings = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    text = strings.get(key, TRANSLATIONS["en"].get(key, key))
    return text.format(**kwargs) if kwargs else text
