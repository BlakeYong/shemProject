from discord_webhook import DiscordWebhook, DiscordEmbed
from shem_configs import shem_configs

class Util:
    def __init__(self):
        utill = None

    
    def send_message(self, text, method = 'error') :
        url = shem_configs[method]
        webhook = DiscordWebhook(url=url)
        embed = DiscordEmbed(title=method, description=str(text), color=242424)
        webhook.add_embed(embed)
        response = webhook.execute()