from icalendar import Calendar as ICal, Event as IEvent
from urllib import request
import datetime, re, os
from typing import List

class Event:

    def __init__(self, summary, description, start_time, end_time):
        self.summary = summary
        self.description = description
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return f"Event\n\tsummary: {self.summary}\n\tdescription: {self.description}\n\tdtstart: {self.start_time}\n\tdtend: {self.end_time}"

class Calendar:

    def __init__(self, calendar_ical_url):
        self._calendar_ical_url = calendar_ical_url

    def _ellipsis(s, maxlen=50):
        return (s[:maxlen] + "...") if len(s) > maxlen else s

    def _escape_rn(s):
        s = re.sub(r"\r", r"\\r", s)
        s = re.sub(r"\n", r"\\n", s)
        return s

    def _dt_to_datetime(dt):
        if isinstance(dt, datetime.datetime):
            return dt
        elif isinstance(dt, datetime.date):
            dt = datetime.datetime.combine(dt, datetime.time.min)
            dt = dt.replace(tzinfo=datetime.timezone.utc)
            return dt
        else:
            raise TypeError(f"Unhandled input type: {type(dt)}")

    def _utc_to_local(dt):
        return dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)

    def _fetch(self):
        req = request.urlopen(self._calendar_ical_url)
        ical_str = req.read()
        ical = ICal.from_ical(ical_str)

        now = datetime.datetime.now(datetime.timezone.utc)
        self.events = []

        for event in ical.walk('vevent'):
            summary = str(event.get("summary"))
            description = Calendar._ellipsis(Calendar._escape_rn(str(event.get("description"))))
            dtstart = Calendar._dt_to_datetime(event.get("dtstart").dt)

            if dtstart.tzinfo is not None:
                if dtstart.tzinfo.utcoffset(dtstart) is not None:
                    print
            if "dtend" not in event:
                dtend = dtstart
            else:
                dtend = Calendar._dt_to_datetime(event.get("dtend").dt)

            if now <= dtend:
                ev = Event(summary, description, Calendar._utc_to_local(dtstart), Calendar._utc_to_local(dtend))
                self.events.append(ev)
        self.events.sort(key=lambda x: x.start_time, reverse=False)

    def find_event(self, event_to_find):
        self._fetch()
        for event in self.events:
            if re.match(r""+event_to_find, event.summary, re.IGNORECASE):
                return event

    def find_events(self, event_to_find) -> List[Event]:
        self._fetch()
        return [event for event in self.events if re.match(r""+event_to_find, event.summary, re.IGNORECASE)]
