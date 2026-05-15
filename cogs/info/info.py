import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
import os


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="info", description="Affiche les infos du bot/serveur/membre")
    @app_commands.describe(
        option="bot, serveur ou membre",
        membre="Le membre (requis si option = membre)"
    )
    @app_commands.choices(option=[
        app_commands.Choice(name="bot", value="bot"),
        app_commands.Choice(name="serveur", value="serveur"),
        app_commands.Choice(name="membre", value="membre")
    ])
    async def info(self, interaction: discord.Interaction, option: app_commands.Choice[str], membre: discord.Member = None):
        """Affiche les infos du bot, serveur ou d'un membre"""
        
        print(f"[DEBUG] Commande /info appelée avec option: {option.value}")
        
        if option.value == "bot":
            await self.bot_info(interaction)
        elif option.value == "serveur":
            await self.server_info(interaction)
        elif option.value == "membre":
            if not membre:
                await interaction.response.send_message("Erreur 312 : Veuillez spécifier un membre", ephemeral=True)
                print("[WARNING] Option membre mais pas de membre spécifié")
                return
            await self.member_info(interaction, membre)

    async def bot_info(self, interaction: discord.Interaction):
        """Affiche les infos du bot"""
        
        print("[DEBUG] Affichage des infos du bot")
        
        # Récupérer l'utilisateur du bot
        bot_user = self.bot.user
        
        # Construire l'embed
        embed = discord.Embed(
            title=f"Infos du Bot - {bot_user.name}",
            color=0x982BDC,
            timestamp=datetime.now()
        )
        
        # Avatar du bot
        try:
            avatar_url = bot_user.display_avatar.with_format("png").url
            embed.set_thumbnail(url=avatar_url)
            print("[DEBUG] Avatar du bot ajouté")
        except Exception as e:
            print(f"[WARNING] Impossible d'ajouter l'avatar du bot: {e}")
        
        # Infos du bot
        try:
            embed.add_field(
                name="Nom",
                value=bot_user.name,
                inline=True
            )
            embed.add_field(
                name="ID",
                value=str(bot_user.id),
                inline=True
            )
            embed.add_field(
                name="Créé le",
                value=bot_user.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                inline=True
            )
            embed.add_field(
                name="Nombre de serveurs",
                value=str(len(self.bot.guilds)),
                inline=True
            )
            embed.add_field(
                name="Nombre d'utilisateurs",
                value=str(sum(guild.member_count for guild in self.bot.guilds)),
                inline=True
            )
            embed.add_field(
                name="Ping",
                value=f"{round(self.bot.latency * 1000)} ms",
                inline=True
            )
            
            print("[DEBUG] Champs du bot ajoutés")
        except Exception as e:
            print(f"[ERROR] Erreur lors de la création des champs du bot: {e}")
        
        try:
            await interaction.response.send_message(embed=embed)
            print("[DEBUG] Embed du bot envoyé")
        except Exception as e:
            print(f"[ERROR] Impossible d'envoyer l'embed du bot: {e}")
            await interaction.response.send_message("Erreur 999 : Impossible d'afficher les infos du bot.", ephemeral=True)

    async def server_info(self, interaction: discord.Interaction):
        """Affiche les infos du serveur"""
        
        print("[DEBUG] Affichage des infos du serveur")
        
        guild = interaction.guild
        
        if not guild:
            await interaction.response.send_message("Erreur 302 : Cette commande ne fonctionne que sur un serveur.", ephemeral=True)
            print("[WARNING] Commande /info serveur utilisée en MP")
            return
        
        # Construire l'embed
        embed = discord.Embed(
            title=f"Infos du Serveur - {guild.name}",
            color=0x982BDC,
            timestamp=datetime.now()
        )
        
        try:
            if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)
                print("[DEBUG] Icon du serveur ajoutée")
        except Exception as e:
            print(f"[WARNING] Impossible d'ajouter l'icon du serveur: {e}")
        
        # Infos du serveur
        try:
            embed.add_field(
                name="Nom",
                value=guild.name,
                inline=True
            )
            embed.add_field(
                name="ID",
                value=str(guild.id),
                inline=True
            )
            embed.add_field(
                name="Propriétaire",
                value=guild.owner.mention if guild.owner else "Inconnu",
                inline=True
            )
            embed.add_field(
                name="Créé le",
                value=guild.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                inline=True
            )
            embed.add_field(
                name="Nombre de membres",
                value=str(guild.member_count),
                inline=True
            )
            embed.add_field(
                name="Nombre de rôles",
                value=str(len(guild.roles)),
                inline=True
            )
            embed.add_field(
                name="Nombre de salons",
                value=str(len(guild.channels)),
                inline=True
            )
            embed.add_field(
                name="Nombre de salons vocaux",
                value=str(len(guild.voice_channels)),
                inline=True
            )
            embed.add_field(
                name="Nombre de catégories",
                value=str(len(guild.categories)),
                inline=True
            )
            embed.add_field(
                name="Niveau de vérification",
                value=guild.verification_level.name,
                inline=True
            )
            embed.add_field(
                name="Région",
                value=str(guild.region) if hasattr(guild, 'region') else "Automatique",
                inline=True
            )
            
            print("[DEBUG] Champs du serveur ajoutés")
        except Exception as e:
            print(f"[ERROR] Erreur lors de la création des champs du serveur: {e}")
        
        try:
            await interaction.response.send_message(embed=embed)
            print("[DEBUG] Embed du serveur envoyé")
        except Exception as e:
            print(f"[ERROR] Impossible d'envoyer l'embed du serveur: {e}")
            await interaction.response.send_message("Erreur 999 : Impossible d'afficher les infos du serveur.", ephemeral=True)

    async def member_info(self, interaction: discord.Interaction, membre: discord.Member):
        """Affiche les infos d'un membre"""
        
        print(f"[DEBUG] Affichage des infos du membre: {membre}")
        
        guild = interaction.guild
        
        if not guild:
            await interaction.response.send_message("Erreur 302 : Cette commande ne fonctionne que sur un serveur.", ephemeral=True)
            print("[WARNING] Commande /info membre utilisée en MP")
            return
        embed = discord.Embed(
            title=f"Infos du Membre - {membre.display_name}",
            color=0x982BDC,
            timestamp=datetime.now()
        )
        
        embed.set_footer(text="root/info.py")
        
        # Avatar du membre
        try:
            avatar_url = membre.display_avatar.with_format("png").url
            embed.set_thumbnail(url=avatar_url)
            print("[DEBUG] Avatar du membre ajouté")
        except Exception as e:
            print(f"[WARNING] Impossible d'ajouter l'avatar du membre: {e}")
        
        # Banner du membre
        try:
            user = await self.bot.fetch_user(membre.id)
            if user.banner:
                embed.set_image(url=user.banner.url)
                print("[DEBUG] Banner du membre ajoutée")
        except Exception as e:
            print(f"[WARNING] Impossible de récupérer la banner: {e}")
        
        # Infos du membre
        try:
            embed.add_field(
                name="Nom",
                value=membre.name,
                inline=True
            )
            embed.add_field(
                name="Pseudo affiché",
                value=membre.display_name,
                inline=True
            )
            embed.add_field(
                name="ID",
                value=str(membre.id),
                inline=True
            )
            embed.add_field(
                name="Bot",
                value="Oui" if membre.bot else "Non",
                inline=True
            )
            embed.add_field(
                name="Créé le",
                value=membre.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                inline=True
            )
            embed.add_field(
                name="A rejoint le",
                value=membre.joined_at.strftime("%d/%m/%Y %H:%M:%S") if membre.joined_at else "Inconnu",
                inline=True
            )
            embed.add_field(
                name="Rôle le plus haut",
                value=membre.top_role.mention,
                inline=True
            )
            embed.add_field(
                name="Administrateur",
                value="Oui" if membre.guild_permissions.administrator else "Non",
                inline=True
            )
            
            # Boost serveur
            if membre.premium_since:
                embed.add_field(
                    name="Boost serveur",
                    value=f"Oui - Depuis {membre.premium_since.strftime('%d/%m/%Y %H:%M:%S')}",
                    inline=True
                )
            else:
                embed.add_field(
                    name="Boost serveur",
                    value="Non",
                    inline=True
                )
            
            print("[DEBUG] Champs du membre ajoutés")
        except Exception as e:
            print(f"[ERROR] Erreur lors de la création des champs du membre: {e}")
        
        try:
            await interaction.response.send_message(embed=embed)
            print(f"[DEBUG] Embed du membre {membre} envoyé")
        except Exception as e:
            print(f"[ERROR] Impossible d'envoyer l'embed du membre: {e}")
            await interaction.response.send_message("Erreur 999 : Impossible d'afficher les infos du membre.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Info(bot))
