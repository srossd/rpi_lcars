import icalendar
import recurring_ical_events
import urllib.request
import datetime

def get_events(url):
    start_date = datetime.datetime.now()
    end_date =   start_date + datetime.timedelta(days=7)

    ical_string = urllib.request.urlopen(url).read()
    calendar = icalendar.Calendar.from_ical(ical_string)
    events = recurring_ical_events.of(calendar).between(start_date, end_date)
    ans = []

    events.sort(lambda x: x["DTSTART"].dt)

    for event in events:
        name = event["SUMMARY"]
        start = event["DTSTART"].dt.strftime('%A %H:%M')
        end = event["DTEND"].dt.strftime('%H:%M')
        ans.append({'name': name, 'start': start, 'end': end})
    
    return ans