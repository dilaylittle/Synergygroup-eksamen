import requests
from bs4 import BeautifulSoup

def scrape_menu():
    url = 'https://hubnordic.madkastel.dk/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the week number
    week_number = None
    week_header = soup.find('h1', class_='has-text-align-center')
    if week_header:
        week_number_text = week_header.text.strip()
        week_number = ''.join(filter(str.isdigit, week_number_text))

    # Extract the menus
    menus = {}
    containers = soup.find_all('div', class_='et_pb_text_inner')
    for container in containers:
        h4 = container.find('h4')
        if h4 and ('Kays' in h4.text or 'HUB2' in h4.text):
            hub_title = h4.text.strip()
            current_day = None
            if hub_title not in menus:
                menus[hub_title] = []
            for element in container.children:
                if element.name == 'p' and element.find('strong'):
                    current_day = element.text.strip()
                    menus[hub_title].append({'day': current_day, 'meals': []})
                elif element.name == 'p' and current_day:
                    menus[hub_title][-1]['meals'].append(element.text.strip())

    return week_number, menus
