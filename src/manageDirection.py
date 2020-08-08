from urllib.parse import quote
import urllib
import ssl
import json
# from googletrans import Translator
from src.util import Util
from shem_configs import shem_configs


class ManageDirection:

    def find_direction(self,origin,destination):
        
        try:
            origin_url = quote(origin)
            destination_url = quote(destination)

            url = "{0}origin={1}&destination={2}&mode=transit&departure_time=now&key={3}".format(shem_configs["google_maps_url"],origin_url,destination_url,shem_configs['google_maps_key'])
        
            request         = urllib.request.Request(url)
            context         = ssl._create_unverified_context()
            response        = urllib.request.urlopen(request, context=context)
            responseText    = response.read().decode('utf-8')
            responseJson    = json.loads(responseText)

            wholeDict = dict(responseJson)

            path = wholeDict["routes"][0]["legs"][0]
            steps = path["steps"]
        
            en = ""

            for step in steps:
                en += step['html_instructions'] + ". "

            translator = Translator()
            result = translator.translate(en, dest="ko")
            result = result.text
            return {"result": result}

        except :
            Util.error_message(tracback.format_exc())    
        