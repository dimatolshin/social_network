import requests

url = 'https://zaycev.net/'
query = {'search_query': 'баста'}
response = requests.get(url, params=query)

print(response.text)