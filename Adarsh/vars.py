# (c) adarsh-goel
import os
from os import getenv, environ
from dotenv import load_dotenv

load_dotenv()

class Var(object):
    MULTI_CLIENT = False
    
    # Safe casting to avoid crashes during startup if variables are missing
    API_ID = int(getenv('API_ID')) if getenv('API_ID') else None
    API_HASH = str(getenv('API_HASH')) if getenv('API_HASH') else None
    BOT_TOKEN = str(getenv('BOT_TOKEN')) if getenv('BOT_TOKEN') else None
    
    name = str(getenv('SESSION_NAME', 'filetolinkbot'))
    SLEEP_THRESHOLD = int(getenv('SLEEP_THRESHOLD', '60'))
    WORKERS = int(getenv('WORKERS', '4'))
    
    BIN_CHANNEL = int(getenv('BIN_CHANNEL')) if getenv('BIN_CHANNEL') else None
    PORT = int(getenv('PORT', 8080))
    BIND_ADRESS = str(getenv('WEB_SERVER_BIND_ADDRESS', '0.0.0.0'))
    PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
    
    OWNER_ID = set(int(x) for x in os.environ.get("OWNER_ID", "8841187568").split() if x.strip().isdigit())  
    NO_PORT = bool(getenv('NO_PORT', False))
    APP_NAME = None
    OWNER_USERNAME = str(getenv('OWNER_USERNAME'))
    
    # Platform Detection (Heroku / Render / Local)
    ON_HEROKU = 'DYNO' in environ
    ON_RENDER = 'RENDER' in environ  # Added Render support

    if ON_RENDER:
        # Render automatically provides RENDER_EXTERNAL_URL (e.g., https://your-app.onrender.com)
        RENDER_URL = getenv('RENDER_EXTERNAL_URL')
        if RENDER_URL:
            # Extract domain name (FQDN) from Render URL
            FQDN = RENDER_URL.replace("https://", "").replace("http://", "").strip("/")
        else:
            FQDN = str(getenv('FQDN', BIND_ADRESS))
    elif ON_HEROKU:
        APP_NAME = str(getenv('APP_NAME'))
        FQDN = f"{APP_NAME}.herokuapp.com" if APP_NAME else str(getenv('FQDN', BIND_ADRESS))
    else:
        FQDN = str(getenv('FQDN', BIND_ADRESS))
    
    HAS_SSL = bool(getenv('HAS_SSL', False))
    if HAS_SSL or ON_RENDER:  # Render uses HTTPS by default
        URL = "https://{}/".format(FQDN)
    else:
        URL = "http://{}/".format(FQDN)
        
    DATABASE_URL = str(getenv('DATABASE_URL')) if getenv('DATABASE_URL') else None
    UPDATES_CHANNEL = str(getenv('UPDATES_CHANNEL', None))
    BANNED_CHANNELS = list(set(int(x) for x in str(getenv("BANNED_CHANNELS", "-1001362659779")).split() if x.strip().isdigit()))
