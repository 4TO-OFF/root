import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
import time
import os


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Test le ping du bot")
    async def ping(self, interaction: discord.Interaction):
        """Exécute un test ping et envoie les résultats"""
        
        print("[DEBUG] Commande /ping appelée")
        
        # le truc long (normalement)
        start_time = time.time()
        print("[DEBUG] Defer de la réponse...")
        await interaction.response.defer()
        ping_ms_1 = round((time.time() - start_time) * 1000)
        print(f"[DEBUG] Ping 1 (defer): {ping_ms_1} ms")
        
        # le truc court (ca marche sur mon ordi)
        ping_ms_2 = round(self.bot.latency * 1000)
        print(f"[DEBUG] Ping 2 (latency): {ping_ms_2} ms")
        
        cog_file = os.path.abspath(__file__)
        print(f"[DEBUG] Cog file: {cog_file}")
        
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(cog_file)))
        print(f"[DEBUG] Root dir: {root_dir}")
        
        ping_image = os.path.join(root_dir, "assets", "ping.png")
        root_image = os.path.join(root_dir, "assets", "root.png")
        
        print(f"[DEBUG] Ping image path: {ping_image}")
        print(f"[DEBUG] Root image path: {root_image}")
        print(f"[DEBUG] Ping image existe: {os.path.exists(ping_image)}")
        print(f"[DEBUG] Root image existe: {os.path.exists(root_image)}")
        
        # embed
        embed = discord.Embed(
            title="Test ping",
            description="Temps de reponse en ms",
            color=0x982BDC,
            timestamp=datetime.now()
        )
        
        embed.set_footer(text="root/ping.py")
        
        files = []
        
        if os.path.exists(ping_image):
            print("[DEBUG] Ajout de l'image ping")
            embed.set_image(url="attachment://ping.png")
            files.append(discord.File(ping_image, filename="ping.png"))
        else:
            print("[DEBUG] Image ping non trouvée")
        
        if os.path.exists(root_image):
            print("[DEBUG] Ajout du thumbnail root")
            embed.set_thumbnail(url="attachment://root.png")
            files.append(discord.File(root_image, filename="root.png"))
        else:
            print("[DEBUG] Image root non trouvée")
        
        # pour les resultats
        embed.add_field(
            name="Test ping : 1",
            value=f"{ping_ms_1} ms",
            inline=True
        )
        embed.add_field(
            name="Test ping : 2",
            value=f"{ping_ms_2} ms",
            inline=False
        )
        
        print("[DEBUG] Envoi du message...")
        # bah si ca envoie pas on sait pas
        await interaction.followup.send(embed=embed, files=files)
        print("[DEBUG] Message envoyé avec succès")


async def setup(bot):
    await bot.add_cog(Ping(bot))
