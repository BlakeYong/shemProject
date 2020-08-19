from discord_webhook import DiscordWebhook, DiscordEmbed
from shem_configs import Config

class Util:
    def __init__(self):
        utill = None
    
    def createTables(table):
        if not table.table_exists(): # 테이블 자동생성
            table.create_table()
    
    def send_message(self, text, method = 'error') :
        url = Config.URLS[method]
        webhook = DiscordWebhook(url=url)
        embed = DiscordEmbed(title=method, description=str(text), color=242424)
        webhook.add_embed(embed)
        response = webhook.execute()

    