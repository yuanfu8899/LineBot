import requests
import json
API_KEY = '[YOUR_API_KEY]'

def GetGif(keyword):
    url='https://api.giphy.com/v1/gifs/random?api_key='+API_KEY+'&tag='+keyword+'&rating=G'
    data=json.loads(requests.get(url).text)
    url=data['data']['image_url']
    return url

if __name__ == "__main__":
    keyword='cat'
    url=GetGif(keyword)
    print(url)
    