from dotenv import dotenv_values


def bot_token() -> str:
    return dotenv_values("..\.env")['BOT_TOKEN']

def mal_user() -> str:
    return dotenv_values("..\.env")['MAL_USERNAME']

def mal_password() -> str:
    return dotenv_values("..\.env")['MAL_PASSWORD']