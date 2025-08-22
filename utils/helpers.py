import discord

def create_embed(title: str = None, description: str = None, color: discord.Color = discord.Color.blue(), footer: str = None):
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    if footer:
        embed.set_footer(text=footer)
    return embed