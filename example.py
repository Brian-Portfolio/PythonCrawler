import requests
from requests_html import HTMLSession
 
url =  "https://eumostwanted.eu/"

 
try:
    session = HTMLSession()
    response = session.get(url)
    title =  response.html.find('.noticesResults', first=True).text
    print(title)
except requests.exceptions.RequestException as e:
    print(e)