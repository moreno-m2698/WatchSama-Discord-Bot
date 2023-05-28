from dotenv import dotenv_values

def bot_token() -> str:
    return dotenv_values(".env")['BOT_TOKEN'] #file path has to be in reference to the one using it

def mal_user() -> str:
    return dotenv_values(".env")['MAL_USERNAME']

def mal_password() -> str:
    return dotenv_values(".env")['MAL_PASSWORD']

