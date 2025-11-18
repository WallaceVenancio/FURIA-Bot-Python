# cogs/pandascore.py
import discord
from discord.ext import commands
import aiohttp
from datetime import datetime
import config

class PandaScoreCog(commands.Cog, name="PandaScore"):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = "https://api.pandascore.co"
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {config.PANDASCORE_TOKEN}"
        }

    @commands.command(name="resultados")
    async def resultados(self, ctx):
        url = f"{self.base_url}/teams/{config.TEAM_ID}/matches?sort=-begin_at&per_page=5&filter[status]=finished"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.status != 200:
                    await ctx.send("❌ Erro ao buscar partidas.")
                    return

                past_matches = await response.json()

                if not isinstance(past_matches, list) or not past_matches:
                    await ctx.send("❌ Nenhuma partida passada encontrada.")
                    return

                past_info = []
                for match in past_matches:
                    opponents = match.get('opponents', [])
                    opponent_names = [op['opponent']['name'] for op in opponents if op['opponent']['id'] != config.TEAM_ID]
                    opponent_name = opponent_names[0] if opponent_names else 'Adversário indefinido'

                    begin_at = match.get('begin_at')
                    begin_at = datetime.fromisoformat(begin_at.replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M') if begin_at else 'Data não definida'

                    winner_data = match.get('winner')
                    winner = winner_data.get('name') if winner_data else 'Indefinido'
                    result = '✅ Vitória' if winner == config.TEAM_NAME else '❌ Derrota'

                    past_info.append(f"Vs {opponent_name} em {begin_at} - {result}")

                past_list = '\n'.join(past_info) if past_info else 'Nenhuma partida passada encontrada.'

                embed = discord.Embed(
                    title=f"📜 Últimos resultados da {config.TEAM_NAME}",
                    color=0x1e1e1e
                )
                embed.add_field(name="Últimos confrontos", value=past_list, inline=False)
                await ctx.send(embed=embed)

    @commands.command(name="agenda")
    async def agenda(self, ctx):
        url = f"{self.base_url}/matches/upcoming?filter[opponent_id]={config.TEAM_ID}&sort=begin_at"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.status != 200:
                    await ctx.send("❌ Erro ao buscar próximas partidas.")
                    return

                upcoming_matches = await response.json()

                if not isinstance(upcoming_matches, list) or not upcoming_matches:
                    await ctx.send("❌ Nenhuma próxima partida encontrada.")
                    return

                upcoming_info = []
                for match in upcoming_matches[:5]:
                    opponents = match.get('opponents', [])
                    opponent_names = [opponent['opponent']['name'] for opponent in opponents if opponent['opponent']['id'] != config.TEAM_ID]
                    opponent_name = opponent_names[0] if opponent_names else 'Adversário indefinido'
                    
                    begin_at = match.get('begin_at')
                    begin_at = datetime.fromisoformat(begin_at.replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M') if begin_at else 'Data não definida'
                    
                    upcoming_info.append(f"Vs {opponent_name} em {begin_at}")

                upcoming_list = '\n'.join(upcoming_info) if upcoming_info else 'Nenhuma partida futura encontrada.'

                embed = discord.Embed(
                    title=f"📅 Próximas partidas da {config.TEAM_NAME}",
                    color=0x1e1e1e
                )
                embed.add_field(name="Próximos confrontos", value=upcoming_list, inline=False)
                await ctx.send(embed=embed)

    @commands.command(name="jogadores")
    async def jogadores(self, ctx):
        embed = discord.Embed(
            title="🧍‍♂️ Qual jogador você quer informações?",
            description="Use .info <nome> para obter os detalhes.\nEx: .info yuurih",
            color=discord.Color.blue()
        )
        embed.add_field(name="Opções disponíveis:", value="yuurih, yekindar, kscerato, chelo, fallen, skullz, molodoy e guerri", inline=False)
        embed.set_footer(text="Use .info <nome> para continuar.")
        await ctx.send(embed=embed)

    @commands.command(name="info")
    async def jogadores_info(self, ctx, nome: str):
        nome = nome.lower()
        url_time = f"{self.base_url}/teams/{config.TEAM_ID}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url_time, headers=self.headers) as response:
                if response.status != 200:
                    await ctx.send("❌ Erro ao buscar dados do time.")
                    return
                data_time = await response.json()

        jogadores = data_time.get("players", [])
        jogador = next((p for p in jogadores if p.get("slug", "").lower() == nome or p.get("name", "").lower() == nome), None)

        if not jogador:
            await ctx.send("❌ Jogador não encontrado no elenco da FURIA.")
            return

        nome_completo = jogador.get("name", "Desconhecido")
        idade = jogador.get("age", "N/A")
        imagem = jogador.get("image_url", "")
        nascimento = jogador.get("birthday", "Não informado")
        nacionalidade = jogador.get("nationality", "N/A")

        bandeiras = {
            "br": "🇧🇷", "us": "🇺🇸", "ua": "🇺🇦", "pl": "🇵🇱", "se": "🇸🇪",
            "dk": "🇩🇰", "de": "🇩🇪", "fr": "🇫🇷", "ca": "🇨🇦", "lv": "🇱🇻", "kz": "🇰🇿", 
        }
        bandeira = bandeiras.get(nacionalidade.lower(), "🏳️")

        embed = discord.Embed(
            title=f"🔎 {jogador.get('full_name', nome_completo)}",
            color=discord.Color.dark_gold()
        )
        if imagem:
            embed.set_thumbnail(url=imagem)

        embed.add_field(name="Nickname", value=nome_completo, inline=True)
        embed.add_field(name="Idade", value=f"{idade} anos" if idade else "N/A", inline=True)
        embed.add_field(name="Nascimento", value=nascimento or "Não informado", inline=True)
        embed.add_field(name="Nacionalidade", value=f"{bandeira} {nacionalidade.upper()}", inline=True)
        embed.set_footer(text="Informações extraídas diretamente do time da FURIA (PandaScore API)")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(PandaScoreCog(bot))