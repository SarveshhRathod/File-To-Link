# (c) adarsh-goel
import os
import sys
import glob
import asyncio

# --- Python 3.12+ compatibility fix for Pyrogram's import-time event loop check ---
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# Monkeypatch asyncio.get_event_loop to return our loop before importing pyrogram
asyncio.get_event_loop = lambda: loop
# ----------------------------------------------------------------------------------

import logging
import importlib
from pathlib import Path
from pyrogram import idle  # Now this won't crash
from .bot import StreamBot
from .vars import Var
from aiohttp import web
from .server import web_server
from .utils.keepalive import ping_server
from Adarsh.bot.clients import initialize_clients

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

# Get files path
ppath = "Adarsh/bot/plugins/*.py"
files = glob.glob(ppath)

async def start_services():
    print('\n')
    print('------------------- Starting Telegram Bot -------------------')
    await StreamBot.start()
    
    bot_info = await StreamBot.get_me()
    StreamBot.username = bot_info.username
    print("------------------------------ DONE ------------------------------")
    print()
    print("---------------------- Initializing Clients ----------------------")
    await initialize_clients()
    print("------------------------------ DONE ------------------------------")
    print('\n')
    print('--------------------------- Importing Plugins ---------------------------')
    
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"Adarsh/bot/plugins/{plugin_name}.py")
            import_path = ".plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["Adarsh.bot.plugins." + plugin_name] = load
            print("Imported => " + plugin_name)
            
    if Var.ON_HEROKU or Var.ON_RENDER:
        print("------------------ Starting Keep Alive Service ------------------")
        print()
        asyncio.create_task(ping_server())
        
    print('-------------------- Initializing Web Server -------------------------')
    app = web.AppRunner(await web_server())
    await app.setup()
    
    bind_address = "0.0.0.0" if (Var.ON_HEROKU or Var.ON_RENDER) else Var.BIND_ADRESS
    await web.TCPSite(app, bind_address, Var.PORT).start()
    
    print('----------------------------- DONE ---------------------------------------------------------------------')
    print('\n')
    print('---------------------------------------------------------------------------------------------------------')
    print(' follow me for more such exciting bots! https://github.com/adarsh-goel')
    print('---------------------------------------------------------------------------------------------------------')
    print('\n')
    print('----------------------- Service Started -----------------------------------------------------------------')
    print('                        bot =>> {}'.format(bot_info.first_name))
    print('                        server ip =>> {}:{}'.format(bind_address, Var.PORT))
    print('                        Owner =>> {}'.format((Var.OWNER_USERNAME)))
    if Var.ON_HEROKU or Var.ON_RENDER:
        print('                        app running on =>> {}'.format(Var.URL))
    print('---------------------------------------------------------------------------------------------------------')
    print('Give a star to my repo https://github.com/adarsh-goel/filestreambot-pro  also follow me for new bots')
    print('---------------------------------------------------------------------------------------------------------')
    await idle()

if __name__ == '__main__':
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        logging.info('----------------------- Service Stopped -----------------------')
