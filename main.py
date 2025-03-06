from telethon import events, TelegramClient
import os
import asyncio

# Replace with your Telegram API credentials
api_id = 27022459
api_hash = '4babbfbfaa665d5fe978908ae5bf1a73'

# Initialize the Telegram client
guessSolver = TelegramClient('saitama/temp', api_id, api_hash)

# Replace with your target chat ID
chatid = -1002464307402  # Update with your target chat ID

from telethon.tl.types import PhotoStrippedSize

async def send_guess_forever():
    """Send /guess command every 10 seconds, consistently."""
    while True:
        try:
            await guessSolver.send_message(entity=chatid, message='/guess')
            print("Sent: /guess")
        except Exception as e:
            print(f"Error sending /guess: {e}")
        await asyncio.sleep(10)  # Wait exactly 10 seconds

@guessSolver.on(events.NewMessage(from_users=572621020, pattern="Who's that pokemon?", chats=(int(chatid)), incoming=True))
async def handle_pokemon_guess(event):
    """Handle Pokémon guessing when a Pokémon-related message appears."""
    for size in event.message.photo.sizes:
        if isinstance(size, PhotoStrippedSize):
            size = str(size)
            for file in os.listdir("cache/"):
                with open(f"cache/{file}", 'r') as f:
                    file_content = f.read()
                if file_content == size:
                    chat = await event.get_chat()
                    Msg = file.split(".txt")[0]
                    await guessSolver.send_message(chat, Msg)
                    print(f"Guessed Pokémon: {Msg}")
                    return

@guessSolver.on(events.NewMessage(from_users=572621020, pattern="The pokemon was ", chats=int(chatid)))
async def update_cache(event):
    """Update cache with the revealed Pokémon."""
    pokemon_name = ((event.message.text).split("The pokemon was **")[1]).split("**")[0]
    with open(f"cache/{pokemon_name}.txt", 'w') as file:
        with open("saitama/cache.txt", 'r') as inf:
            cont = inf.read()
            file.write(cont)
    os.remove("saitama/cache.txt")
    print(f"Updated cache with Pokémon: {pokemon_name}")

async def main():
    """Start the client and handle periodic tasks."""
    await guessSolver.start()
    print("Client started. Sending /guess every 10 seconds and handling Pokémon guessing.")
    
    # Start the periodic /guess sender
    asyncio.create_task(send_guess_forever())
    
    # Keep the client running to listen for events
    await guessSolver.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
