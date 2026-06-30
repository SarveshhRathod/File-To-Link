# (c) adarsh-goel

import asyncio
import logging
from ..vars import Var
from pyrogram import Client
from Adarsh.utils.config_parser import TokenParser
from . import multi_clients, work_loads, StreamBot

async def initialize_clients():
    multi_clients[0] = StreamBot
    work_loads[0] = 0
    all_tokens = TokenParser().parse_from_env()
    
    if not all_tokens:
        print("No additional clients found, using default client")
        return
    
    async def start_client(client_id, token):
        try:
            print(f"Starting - Client {client_id}")
            if client_id == len(all_tokens):
                await asyncio.sleep(2)
                print("This will take some time, please wait...")
            
            # Updated for Pyrogram v2 compatibility (in_memory=True)
            client = Client(
                name=f"client_{client_id}",
                in_memory=True,
                api_id=Var.API_ID,
                api_hash=Var.API_HASH,
                bot_token=token,
                sleep_threshold=Var.SLEEP_THRESHOLD,
                no_updates=True,
            )
            await client.start()
            work_loads[client_id] = 0
            return client_id, client
        except Exception:
            logging.error(f"Failed starting Client - {client_id} Error:", exc_info=True)
            return None  # Explicitly return None on failure

    # Gather all clients
    results = await asyncio.gather(*[start_client(i, token) for i, token in all_tokens.items()])
    
    # Filter out None values to prevent dict() conversion crash
    valid_clients = [res for res in results if res is not None]
    
    multi_clients.update(dict(valid_clients))
    
    if len(multi_clients) != 1:
        Var.MULTI_CLIENT = True
        print("Multi-Client Mode Enabled")
    else:
        print("No additional clients were initialized, using default client")
