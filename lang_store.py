"""In-memory per-user language preference. Resets on restart, same tradeoff
as game_store.py."""

_user_lang: dict = {}


def get(user_id: int, default: str = "en") -> str:
    return _user_lang.get(user_id, default)


def set(user_id: int, lang: str) -> None:
    _user_lang[user_id] = lang


def has(user_id: int) -> bool:
    return user_id in _user_lang
