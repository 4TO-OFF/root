#arrete de regarder le code nan ?
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# token (dans le .env mets TOKEN="bah ton token trdbl")
load_dotenv()
TOKEN = os.getenv("TOKEN")

# pour les chemins la
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COGS_FILE = os.path.join(BASE_DIR, "cogs.txt")

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# pour les cogs (pour eviter d'avoir 40000 ligne de code)
async def load_cogs():
    if not os.path.exists(COGS_FILE):
        print("[ERROR] cogs.txt introuvable")
        return

    with open(COGS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        cog_path = line.strip()

        # pour l'unqiue commentaire dedans
        if not cog_path or cog_path.startswith("#"):
            continue

        try:
            module = cog_path.replace("/", ".").replace("\\", ".")

            if module.endswith(".py"):
                module = module[:-3]

            await bot.load_extension(module)

            print(f"[INFO] Chargé : {module}")

        except Exception as e:
            print(f"[ERROR] Impossible de charger {cog_path}")
            print(e)

@bot.event
async def on_ready():
    print(f"C'est on (le main marche mais le reste jsp)")
    try:
        synced = await bot.tree.sync()
        print(f"[INFO] {len(synced)} commande(s) slash synchronisée(s)")
    except Exception as e:
        print(f"[ERROR] Erreur lors de la synchronisation des slash commands")
        print(e)

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

import asyncio
asyncio.run(main())