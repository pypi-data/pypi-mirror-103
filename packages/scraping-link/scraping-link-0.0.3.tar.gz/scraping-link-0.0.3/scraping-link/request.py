import requests
import urllib

class ScrapingLinkRequest():

    def scrape(url, apikey, render=0):
        response = requests.get(f'https://app.scraping.link/api/scrape?api_token={apikey}&url={urllib.parse.quote(url)}&render={render}')
        
        return response
