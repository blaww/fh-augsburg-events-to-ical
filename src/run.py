import requests
import datetime
import re
from ics import Calendar, Event
from bs4 import BeautifulSoup

def parse_date(begin: str, end: str) -> str, str:
    begin_date = datetime.datetime.strptime(begin, '%d.%m.%Y, %H:%M').strftime('%Y-%m-%d')
    begin_time = datetime.datetime.strptime(begin, '%d.%m.%Y, %H:%M').strftime('%H:%M')

    end_date = None
    end_time = None
    if "," in end:
        end_date = datetime.datetime.strptime(end, '%d.%m.%Y, %H:%M').strftime('%Y-%m-%d')
        end_time = datetime.datetime.strptime(end, '%d.%m.%Y, %H:%M').strftime('%H:%M')
    else:
        end_date = begin_date
        end_time = end

    return f"{begin_date} {begin_time}", f"{end_date} {end_time}"

url = "https://www.hs-augsburg.de/Gestaltung/Aktuelles.html"
req = requests.get(url)
html = BeautifulSoup(req.content, 'html.parser')

event_section = html.find("div", class_="entry entitylistentry event")
event_list = event_section.find_all('div', attrs={'data-key' : True})

calendar = Calendar()

for event_html in event_list:
    event = Event()
    event.name = event_html.find("h3", class_="hyphenate").find("a").text

    if "Entfällt" in event.name:
        continue

    event.url = "https://www.hs-augsburg.de/Gestaltung/" + event_html.find("h3", class_="hyphenate").find("a")['href']

    date = event_html.find("h4", class_="date").text.replace("Uhr", "")
    date_begin, date_end = date.split("-")
    event.begin, event.end = parse_date(re.sub(' +', ' ', date_begin).strip(), re.sub(' +', ' ', date_end).strip())

    calendar.events.add(event)

with open('/app/out/events.ics', 'w') as f:
    f.writelines(calendar)