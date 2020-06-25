import requests
import datetime
import re

from ics import Calendar, Event
from bs4 import BeautifulSoup


def parse_date(begin: str, end: str) -> str, str:
    """
        Accepts two dates as string in the following format: `01.01.2020, 20:00`.

        Returns the two dates in the following format: `2020-01-01 20:00`.

        If the second given date only contains a time the date of the first given date will be used.
    """
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


# load the html
url = "https://www.hs-augsburg.de/Gestaltung/Aktuelles.html"
req = requests.get(url)
html = BeautifulSoup(req.content, 'html.parser')

# get the event html tag
event_section = html.find("div", class_="entry entitylistentry event")
event_list = event_section.find_all('div', attrs={'data-key' : True})

# create a calendar instance
calendar = Calendar()

# loop over the events html blocks, create an event for each of them and add it to the calendar
for event_html in event_list:
    event = Event()

    # get the events name
    event.name = event_html.find("h3", class_="hyphenate").find("a").text

    # check if event is marked as "dropped"
    if "Entfällt" in event.name:
        continue
    
    # build the events url
    event.url = "https://www.hs-augsburg.de/Gestaltung/" + event_html.find("h3", class_="hyphenate").find("a")['href']

    # find and parse begin & end date
    date = event_html.find("h4", class_="date").text.replace("Uhr", "")
    date_begin, date_end = date.split("-")
    event.begin, event.end = parse_date(re.sub(' +', ' ', date_begin).strip(), re.sub(' +', ' ', date_end).strip())

    # add event to calendar
    calendar.events.add(event)

# save calendar to file
with open('/app/out/events.ics', 'w') as f:
    f.writelines(calendar)