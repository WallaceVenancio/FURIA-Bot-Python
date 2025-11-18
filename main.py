import discord
from discord.ext import commands
import requests
import aiohttp 
from discord import Embed
from datetime import datetime

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

@bot.command()
async def loja(ctx: commands.Context):
    loja_embed = discord.Embed(
        title="🎯 CHEGOU A HORA DE VESTIR A FÚRIA!",
        description=(
            "A nova coleção da FURIA em parceria com a Adidas já está disponível! "
            "É estilo, performance e atitude juntos numa linha exclusiva que representa a garra e a identidade da nossa matilha.\n\n"
            "Seja nas ruas, nos games ou nos estádios, vista FURIA, vista Adidas.\n\n"
            "🔥 Porque ser FURIA é um estilo de vida.\n\n"
            "🛒 Visite agora mesmo a nossa loja oficial e garanta os novos produtos da collab:\n"
            "👉 https://www.furia.gg/"
        ),
        color=0x1e1e1e
    )

    loja_embed.set_thumbnail(
        url="https://images-ext-1.discordapp.net/external/niDaU9KlaUOdFrWP6lU2uRa7F85mZxXFSUxFBirBE1M/https/pbs.twimg.com/profile_images/1774820117538295808/xilo38_v_400x400.png?format=webp&quality=lossless"
    )

    imagem = discord.File("imagens/Furia-adidas.png", filename="loja_adidas.png")
    loja_embed.set_image(url="attachment://loja_adidas.png")

    await ctx.reply(embed=loja_embed, file=imagem)

@bot.command()
async def redes(ctx: commands.Context):
    embed = discord.Embed(
        title="🌐 Nossas Redes Sociais",
        description="Acompanhe a FURIA nas principais plataformas:",
        color=0x1e1e1e
    )
    embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/niDaU9KlaUOdFrWP6lU2uRa7F85mZxXFSUxFBirBE1M/https/pbs.twimg.com/profile_images/1774820117538295808/xilo38_v_400x400.png?format=webp&quality=lossless")

    embed.add_field(
        name="<:Instagram:1367620578118340658> Instagram",
        value="[Clique aqui!](https://www.instagram.com/furiagg)",
        inline=False
    )
    embed.add_field(
        name="<:Twitter:1367617917679566979> Twitter",
        value="[Clique aqui!](https://x.com/furia)",
        inline=False
    )
    embed.add_field(
        name=f"<:Youtube:1367618017697206293> YouTube",
        value="[Clique aqui!](https://www.youtube.com/@FURIAgg)",
        inline=False
    )
    embed.add_field(
        name="<:Twitch:1367618084378116176> Twitch",
        value="[Clique aqui!](https://www.twitch.tv/furiatv)",
        inline=False
    )
    embed.add_field(
        name="<:tiktok:1367617974856585226> Tik Tok",
        value="[Clique aqui!](https://www.tiktok.com/@furia)",
        inline=False
    )
    embed.set_footer(text="Clique nos links para nos seguir!")
    await ctx.reply(embed=embed)


@bot.command()
async def furia(ctx:commands.Context):
    meu_embed = discord.Embed()
    meu_embed.description = " Furia **(estilizado FURIA)** é uma organização brasileira que atua nas modalidades de e-sports em **Counter-Strike 2**, **Rocket League**, **League of Legends**, **Valorant**, **Rainbow Six: Siege**, **Apex Legends**, e Futebol de 7 **(Kings League)**. Fundada em 2017 em Uberlandia, a FURIA possui o time de Counter-Strike que melhor desempenha nas competições internacionais mais recentes, sempre a frente nas colocações entre equipes do país.\n\n A organização foi eleita por dois anos consecutivos, em **2020 e 2021**, como a melhor organização de esportes eletrônicos no **Prêmio eSports Brasil**. Em 2022, foi apontada como a **quinta maior organização de esportes eletrônicos do mundo** pelo portal norte-americano Nerd Street.\n\n"

    logo = discord.File("imagens/campeoes.png", "cs_campeoes.png")
    meu_embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/niDaU9KlaUOdFrWP6lU2uRa7F85mZxXFSUxFBirBE1M/https/pbs.twimg.com/profile_images/1774820117538295808/xilo38_v_400x400.png?format=webp&quality=lossless")
    meu_embed.set_image(url="attachment://cs_campeoes.png")
    meu_embed.set_author(name="Quem Somos?", url="https://www.furia.gg/quem-somos")
    meu_embed.set_footer(text="Unimos pessoas e alimentamos sonhos dentro e fora dos jogos.")
    await ctx.reply(embed=meu_embed, file=logo)


@bot.command(name="resultados")  # Para as partidas passadas da FURIA CS
async def resultados(ctx):
    team_id = 124530
    team_name = "FURIA"
    token = "c_7e8vUuX8obYa9cMc1ozj7jSTa7ZQjlJ4Wsovl7L2EzdLoxFCQ"

    url = f"https://api.pandascore.co/teams/{team_id}/matches?sort=-begin_at&per_page=5&filter[status]=finished" # Paginação ajustada para pegar as últimas 5 partidas
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Requisição assíncrona com aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
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
                opponent_names = [op['opponent']['name'] for op in opponents if op['opponent']['id'] != team_id]
                opponent_name = opponent_names[0] if opponent_names else 'Adversário indefinido'

                begin_at = match.get('begin_at')
                begin_at = datetime.fromisoformat(begin_at.replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M') if begin_at else 'Data não definida'

                winner_data = match.get('winner')
                winner = winner_data.get('name') if winner_data else 'Indefinido'
                result = '✅ Vitória' if winner == team_name else '❌ Derrota'

                past_info.append(f"Vs {opponent_name} em {begin_at} - {result}")

            past_list = '\n'.join(past_info) if past_info else 'Nenhuma partida passada encontrada.'

            # Enviar com Embed
            embed = discord.Embed(
                title=f"📜 Últimos resultados da {team_name}",
                color=0x1e1e1e
            )
            embed.add_field(
                name="Últimos confrontos",
                value=past_list,
                inline=False
            )
            await ctx.send(embed=embed)

@bot.command(name="agenda")  # Para as próximas partidas da FURIA CS
async def agenda(ctx):
    team_id = 124530
    team_name = "FURIA"
    token = "c_7e8vUuX8obYa9cMc1ozj7jSTa7ZQjlJ4Wsovl7L2EzdLoxFCQ"

    upcoming_url = f"https://api.pandascore.co/matches/upcoming?filter[opponent_id]={team_id}&sort=begin_at&token={token}"
    headers = {"Accept": "application/json"}
    upcoming_response = requests.get(upcoming_url, headers=headers)

    if upcoming_response.status_code != 200:
        await ctx.send("❌ Erro ao buscar próximas partidas.")
        return

    upcoming_matches = upcoming_response.json()

    if not isinstance(upcoming_matches, list) or not upcoming_matches:
        await ctx.send("❌ Nenhuma próxima partida encontrada.")
        return

    upcoming_info = []
    for match in upcoming_matches[:5]:
        opponents = match.get('opponents', [])
        opponent_names = [opponent['opponent']['name'] for opponent in opponents if opponent['opponent']['id'] != team_id]
        opponent_name = opponent_names[0] if opponent_names else 'Adversário indefinido'
        
        begin_at = match.get('begin_at')
        if begin_at:
            begin_at = datetime.fromisoformat(begin_at.replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M')
        else:
            begin_at = 'Data não definida'
        
        upcoming_info.append(f"Vs {opponent_name} em {begin_at}")

    upcoming_list = '\n'.join(upcoming_info) if upcoming_info else 'Nenhuma partida futura encontrada.'

    # Enviar com Embed
    embed = discord.Embed(
        title=f"📅 Próximas partidas da {team_name}",
        color=0x1e1e1e
    )
    embed.add_field(
        name="Próximos confrontos",
        value=upcoming_list,
        inline=False
    )
    await ctx.send(embed=embed)

@bot.command(name="jogadores")
async def jogadores(ctx):
    embed = discord.Embed(
        title="🧍‍♂️ Qual jogador você quer informações?",
        description="Use .info <nome> para obter os detalhes.\nEx: .info yuurih",
        color=discord.Color.blue()
    )
    embed.add_field(name="Opções disponíveis:", value="yuurih, yekindar, kscerato, chelo, fallen, skullz, molodoy e guerri", inline=False)
    embed.set_footer(text="Use .info <nome> para continuar.")
    await ctx.send(embed=embed)

@bot.command(name="info")
async def jogadores_info(ctx, nome: str):
    nome = nome.lower()

    # Buscar os jogadores da FURIA (time ID 124530)
    url_time = "https://api.pandascore.co/teams/124530?token=c_7e8vUuX8obYa9cMc1ozj7jSTa7ZQjlJ4Wsovl7L2EzdLoxFCQ"
    headers = {"Accept": "application/json"}
    response_time = requests.get(url_time, headers=headers)

    if response_time.status_code != 200:
        await ctx.send("❌ Erro ao buscar dados do time.")
        return

    data_time = response_time.json()
    jogadores = data_time.get("players", [])

    # Tenta encontrar o jogador pelo nickname
    jogador = next((p for p in jogadores if p.get("slug", "").lower() == nome or p.get("name", "").lower() == nome), None)

    if not jogador:
        await ctx.send("❌ Jogador não encontrado no elenco da FURIA.")
        return

    nome_completo = jogador.get("name", "Desconhecido")
    apelido = jogador.get("slug", "N/A")
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

@bot.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(
        title="📖 Lista de Comandos do Bot da FURIA",
        description="Confira abaixo todos os comandos disponíveis:",
        color=0x1e1e1e
    )
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1774820117538295808/xilo38_v_400x400.png")

    embed.add_field(name=".loja", value="🛍️ Mostra a coleção da FURIA com a Adidas.", inline=False)
    embed.add_field(name=".redes", value="📱 Mostra as redes sociais oficiais da FURIA.", inline=False)
    embed.add_field(name=".furia", value="🐺 Informações sobre a organização FURIA.", inline=False)
    embed.add_field(name=".resultados", value="📜 Últimos resultados da FURIA CS.", inline=False)
    embed.add_field(name=".agenda", value="🗓️ Próximos confrontos da FURIA CS.", inline=False)
    embed.add_field(name=".jogadores", value="👥 Lista os jogadores disponíveis para ver info.", inline=False)
    embed.add_field(name=".info <nome>", value="ℹ️ Informações detalhadas de um jogador da FURIA.", inline=False)

    embed.set_footer(text="Use um comando com o prefixo '.' para começar. Ex: .loja")
    await ctx.send(embed=embed)


bot.run ("MTM2NTA3OTIxMTk4MjcxNzA0MQ.GqpKtN.IeMoJhrsO9yCtcnHLbSYCennsGxJoIlY0-p_UM")