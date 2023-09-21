from dotenv import dotenv_values

class App_Config():

   

    @staticmethod
    def bot_token() -> str:
        return dotenv_values(".env")['BOT_TOKEN'] #file path has to be in reference to the one using it

    @staticmethod
    def mal_user() -> str:
        return dotenv_values(".env")['MAL_USERNAME']

    @staticmethod
    def mal_password() -> str:
        return dotenv_values(".env")['MAL_PASSWORD']

    @staticmethod
    def my_guild() -> int:
        
        guild_Id = dotenv_values(".env")["MY_GUILD"]
        try:
            result = int(guild_Id)
            return result
        
        except TypeError:
            print("Guild ID cannot resolve to int")
        
        except: 
            print("Something else went wrong")

