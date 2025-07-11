import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
import random
import asyncio
import time
import datetime
import re
import subprocess
import sys
import traceback
from discord.utils import get
from keep_alive import keep_alive
from discord.ui import Button, View
from discord.ui import View, Select
from discord.ui import Modal, TextInput
from discord.ext import tasks
from collections import defaultdict
from collections import deque
from datetime import datetime, timedelta
import psutil
import platform

token = os.environ['SHADOW']
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.moderation = True  # <- Pour certains wrappers ou futures versions
start_time = time.time()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="-", intents=intents, help_command=None)

@bot.event
async def on_ready():
    global start_time
    start_time = time.time()  # Défini l'heure de démarrage lorsque le bot est prêt
    print(f'{bot.user} est prêt et l\'uptime est maintenant calculable.')
    print(f"✅ Le bot {bot.user} est maintenant connecté ! (ID: {bot.user.id})")
    print(f"✅ Connecté en tant que {bot.user}")
    await bot.wait_until_ready()
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))  # Sync local au serveur
        print(f"🔧 {len(synced)} commande(s) slash synchronisée(s).")
    except Exception as e:
        print(f"❌ Erreur de synchronisation : {e}")
    
    await clear_panel_channel()
    await send_ticket_panel()

    guild = discord.Object(id='946034497219100723')
    await bot.tree.sync(guild=guild)
    print(f"Commandes synchronisées pour le serveur {guild.id}")



    # Initialisation de l'uptime du bot
    bot.uptime = time.time()
    
    # Récupération du nombre de serveurs et d'utilisateurs
    guild_count = len(bot.guilds)
    member_count = sum(guild.member_count for guild in bot.guilds)
    
    # Affichage des statistiques du bot dans la console
    print(f"\n📊 **Statistiques du bot :**")
    print(f"➡️ **Serveurs** : {guild_count}")
    print(f"➡️ **Utilisateurs** : {member_count}")
    
    # Liste des activités dynamiques
    activity_types = [
        discord.Activity(type=discord.ActivityType.watching, name="La lune de sang 🌕!"),
        discord.Activity(type=discord.ActivityType.streaming, name="L'Autre Monde 🪐"),
        discord.Activity(type=discord.ActivityType.streaming, name="Shadow Garden"),
    ]
    
    # Sélection d'une activité au hasard
    activity = random.choice(activity_types)
    
    # Choix d'un statut aléatoire
    status_types = [discord.Status.online, discord.Status.idle, discord.Status.dnd]
    status = random.choice(status_types)
    
    # Mise à jour du statut et de l'activité
    await bot.change_presence(activity=activity, status=status)
    
    print(f"\n🎉 **{bot.user}** est maintenant connecté et affiche ses statistiques dynamiques avec succès !")

    # Afficher les commandes chargées
    print("📌 Commandes disponibles 😊")
    for command in bot.commands:
        print(f"- {command.name}")

    try:

    # Synchroniser les commandes avec Discord
        synced = await bot.tree.sync()  # Synchronisation des commandes slash
        print(f"✅ Commandes slash synchronisées : {[cmd.name for cmd in synced]}")
    except Exception as e:
        print(f"❌ Erreur de synchronisation des commandes slash : {e}")

    # Jongler entre différentes activités et statuts
    while True:
        for activity in activity_types:
            for status in status_types:
                await bot.change_presence(status=status, activity=activity)
                await asyncio.sleep(10)  # Attente de 10 secondes avant de changer l'activité et le statut
    for guild in bot.guilds:
        GUILD_SETTINGS[guild.id] = load_guild_settings(guild.id)

# Token pour démarrer le bot (à partir des secrets)
# Lancer le bot avec ton token depuis l'environnement  
keep_alive()
bot.run(token)
