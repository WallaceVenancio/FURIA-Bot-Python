import discord
from discord.ext import commands
import asyncio
import os
import config

class FuriaBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # Necessário para ler o conteúdo das mensagens
        super().__init__(command_prefix=".", intents=intents, help_command=None)

    async def setup_hook(self):
        """Carrega as extensões (cogs) automaticamente."""
        cogs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cogs')
        for filename in os.listdir(cogs_path):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f"✅ Cog '{filename[:-3]}' carregado com sucesso.")
                except Exception as e:
                    print(f"❌ Falha ao carregar o cog '{filename[:-3]}'. Erro: {e}")

    async def on_ready(self):
        print(f'🚀 Bot conectado como {self.user}')
        print(f'ID do Bot: {self.user.id}')

async def main():
    bot = FuriaBot()
    await bot.start(config.DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())