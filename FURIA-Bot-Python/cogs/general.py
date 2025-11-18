# cogs/general.py
import discord
from discord.ext import commands

class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def loja(self, ctx: commands.Context):
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
        loja_embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/niDaU9KlaUOdFrWP6lU2uRa7F85mZxXFSUxFBirBE1M/https/pbs.twimg.com/profile_images/1774820117538295808/xilo38_v_400x400.png?format=webp&quality=lossless")
        imagem = discord.File("imagens/Furia-adidas.png", filename="loja_adidas.png")
        loja_embed.set_image(url="attachment://loja_adidas.png")
        await ctx.reply(embed=loja_embed, file=imagem)

    @commands.command()
    async def redes(self, ctx: commands.Context):
        embed = discord.Embed(
            title="🌐 Nossas Redes Sociais",
            description="Acompanhe a FURIA nas principais plataformas:",
            color=0x1e1e1e
        )
        embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/niDaU9KlaUOdFrWP6lU2uRa7F85mZxXFSUxFBirBE1M/https/pbs.twimg.com/profile_images/1774820117538295808/xilo38_v_400x400.png?format=webp&quality=lossless")
        embed.add_field(name="<:Instagram:1367620578118340658> Instagram", value="[Clique aqui!](https://www.instagram.com/furiagg)", inline=False)
        embed.add_field(name="<:Twitter:1367617917679566979> Twitter", value="[Clique aqui!](https://x.com/furia)", inline=False)
        embed.add_field(name=f"<:Youtube:1367618017697206293> YouTube", value="[Clique aqui!](https://www.youtube.com/@FURIAgg)", inline=False)
        embed.add_field(name="<:Twitch:1367618084378116176> Twitch", value="[Clique aqui!](https://www.twitch.tv/furiatv)", inline=False)
        embed.add_field(name="<:tiktok:1367617974856585226> Tik Tok", value="[Clique aqui!](https://www.tiktok.com/@furia)", inline=False)
        embed.set_footer(text="Clique nos links para nos seguir!")
        await ctx.reply(embed=embed)

    @commands.command()
    async def furia(self, ctx:commands.Context):
        meu_embed = discord.Embed(
            description=" Furia **(estilizado FURIA)** é uma organização brasileira que atua nas modalidades de e-sports em **Counter-Strike 2**, **Rocket League**, **League of Legends**, **Valorant**, **Rainbow Six: Siege**, **Apex Legends**, e Futebol de 7 **(Kings League)**. Fundada em 2017 em Uberlandia, a FURIA possui o time de Counter-Strike que melhor desempenha nas competições internacionais mais recentes, sempre a frente nas colocações entre equipes do país.\n\n A organização foi eleita por dois anos consecutivos, em **2020 e 2021**, como a melhor organização de esportes eletrônicos no **Prêmio eSports Brasil**. Em 2022, foi apontada como a **quinta maior organização de esportes eletrônicos do mundo** pelo portal norte-americano Nerd Street.\n\n"
        )
        logo = discord.File("imagens/campeoes.png", "cs_campeoes.png")
        meu_embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/niDaU9KlaUOdFrWP6lU2uRa7F85mZxXFSUxFBirBE1M/https/pbs.twimg.com/profile_images/1774820117538295808/xilo38_v_400x400.png?format=webp&quality=lossless")
        meu_embed.set_image(url="attachment://cs_campeoes.png")
        meu_embed.set_author(name="Quem Somos?", url="https://www.furia.gg/quem-somos")
        meu_embed.set_footer(text="Unimos pessoas e alimentamos sonhos dentro e fora dos jogos.")
        await ctx.reply(embed=meu_embed, file=logo)

    @commands.command(name="help")
    async def help_command(self, ctx):
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


async def setup(bot):
    await bot.add_cog(GeneralCog(bot))