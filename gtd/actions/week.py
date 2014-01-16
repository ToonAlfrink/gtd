"""
Various functions to provide a good overview of upcoming scheduled stuff
(Right now this just prints the upcoming week which is 90% of what i need)
"""

from gtd.actions.models import RecurrentAction
from gtd.tools import CronEntry

from datetime import date, datetime, timedelta, time
from pprint import pprint


def printout(actions):
    weekday = None
    for _time, action in actions:
        end_time = _time + timedelta(minutes = action.duration)
        weekday_new = _time.strftime("%A")[:3].upper()
        if weekday_new != weekday:
            weekday = weekday_new
            print
        print("{weekday} {_time.hour:02d}:{_time.minute:02d} - {end_time.hour:02d}:{end_time.minute:02d} -> {action.name}".format(**locals()))



def today():
    """Prints an overview of today's scheduled actions"""
    actions_today = []
    actions = RecurrentAction.objects.all()
    d1 = datetime.combine(date.today(), time(0,0))
    d2 = d1 + timedelta(days = 7)
    for action in actions:
        for o in action.cronhandler.occurs_between(d1, d2):
            actions_today.append((o, action))
    actions_today = sorted(actions_today)
    printout(actions_today)

def thisweek():
    """Prints an overview of the upcoming 7 day's scheduled actions"""
    actions_thisweek = []
    actions = RecurrentAction.objects.filter(done = False)
    d1 = datetime.combine(date.today(), time(0,0))
    d2 = d1 + timedelta(days = 7)
    for action in actions:
        upcoming = action.cronhandler.next()
        if not upcoming or upcoming > datetime(2100,1,1):
            action.done = True
            action.save()
        for o in action.cronhandler.occurs_between(d1, d2):
            actions_thisweek.append((o, action))
    actions_thisweek = sorted(actions_thisweek)
    printout(actions_thisweek)

if __name__ == "__main__":
    thisweek()
    
    
