import datetime, re, os, pytest
from base.calendar_parser import Calendar, Event

def test_event():
    now = datetime.datetime.now(datetime.timezone.utc)
    s = 'summary'
    d = 'description'
    ev = Event(s, d, now, now)
    assert ev.summary == s
    assert ev.description == d

def test_calender(): #TODO
    cal = Calendar('https://calendar.google.com/calendar/ical/makerspace.se_dsd75rv0l7rblcq1sd627fab38%40group.calendar.google.com/public/basic.ics')
    cal._fetch()
