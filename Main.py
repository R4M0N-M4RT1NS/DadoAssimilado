from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands
from responses import get_response

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# SETUP
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# MENSAGEM DE AJUDA
HELP_TEXT = (
    "🎲 **Como usar o bot de dados:**  🎲\n\n"
    "• Use `XdY` para rolar dados (ex: `2d6`, `1d20`, `3d4+2`)\n"
    "• Use `!XdY` para ativar o modo especial de Assimilação, se o dado for d6, d10 ou d12\n"
    "• Use `N#XdY` para repetir a mesma rolagem múltiplas vezes (ex: `3#1d10`)\n"
    "• Suporta operações matemáticas: `+`, `-`, `*`, `/`\n"
    "• Exemplo: `2d6+3` ou `!1d12`\n\n"
    "Agora é só rolar (Não hunin, não é um trocadilho)\n"
    "- by Cabriteiro"
)

# COMANDO DE SLASH /help
@bot.tree.command(name="help", description="Mostra como usar o bot de dados.")
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message(HELP_TEXT, ephemeral=False)

# EVENTO: quando o bot estiver pronto
@bot.event
async def on_ready():
    await bot.tree.sync()  # Sincroniza os comandos de barra com o Discord
    print(f'Bot {bot.user} está online!')

# EVENTO: mensagem recebida
@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    user_message = message.content
    if not user_message:
        return

    response = get_response(user_message)
    if response:
        try:
            await message.reply(response)
        except Exception as e:
            print(f"Erro ao responder mensagem: {e}")

bot.run(TOKEN)
