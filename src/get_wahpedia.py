import requests

url = "https://wahapedia.ru/aos4/factions/skaven/Clanrats"
response = requests.get(url, timeout=10)
response.raise_for_status()

html = response.text  # decoded HTML

with open("src/ui/wahpedia_warscroll_clanrats.html", "w", encoding="utf-8") as f:
    f.write(html)