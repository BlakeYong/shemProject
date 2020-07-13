from discord_webhook import DiscordWebhook, DiscordEmbed
from shem_configs import shem_configs

url = shem_configs['webhook']

class Util:
    def __init__(self):
        utill = None
    
    def createTables(table):
        if not table.table_exists(): # 테이블 자동생성
            table.create_table()

    
    def error_message(self,text) :
        
        webhook = DiscordWebhook(url=url)
        embed = DiscordEmbed(title="Error", description=str(text), color=242424)
        webhook.add_embed(embed)
        response = webhook.execute()
        