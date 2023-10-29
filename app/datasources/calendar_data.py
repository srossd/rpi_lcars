import icalendar
import recurring_ical_events
import urllib.request
import datetime

def get_events():
    start_date = datetime.datetime.now()
    end_date =   start_date + datetime.timedelta(days=30)
    url = "https://calendar.google.com/calendar/ical/rossd97%40gmail.com/private-27770a2b812b19fdb1bf9b99f7da7de8/basic.ics"

    ical_string = urllib.request.urlopen(url).read()
    calendar = icalendar.Calendar.from_ical(ical_string)
    events = recurring_ical_events.of(calendar).between(start_date, end_date)
    ans = []

    for event in events:
        name = event["SUMMARY"]
        start = event["DTSTART"].dt.strftime('%A %H:%M')
        end = event["DTEND"].dt.strftime('%H:%M')
        ans.append({'name': name, 'start': start, 'end': end})
    
    return ans