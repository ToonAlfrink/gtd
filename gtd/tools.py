def inp(prompt, constraints = []):
    while True:
        x = raw_input(prompt + "\n> ")
        fail = False
        for c in constraints:
            if not eval(c):
                print("'{c}' not met".format(**locals()))
                fail = True
        if not fail:
            return x
        else:
            print("Try again")


from datetime import timedelta, datetime, time

class CronEntry(object):
    def __init__(self, cron):
        self.cron = cron
        self.datepointer = datetime.now()

    def date_match(self, date):
        """
        Will this cron fire at the given date?
        """
        data = self._parse_cron()
        constraints = [
            "date.year in data['year']",
            "date.month in data['month']",
            "date.weekday() in data['weekday']",
            "date.day in data['day']"]
        for c in constraints:
            if not eval(c):
                return False
        return True

    def time_match(self, time):
        """
        Will this cron fire at the given time?
        """
        data = self._parse_cron()
        if time.hour in data['hour'] and time.minute in data['minute']:
            return True
        return False

    def next(self):
        """
        the next date at which this cron will fire
        returns None if it won't in the next 100 years
        """
        # Add a minute
        self.datepointer += timedelta(minutes = 1)

        # Check remaining minutes of the day
        midnight = datetime.combine(datetime.date(self.datepointer) + timedelta(days = 1), time(0,0))
        for x in range(int((midnight - self.datepointer).seconds / 60)):
            self.datepointer += timedelta(minutes = 1)
            if self.date_match(self.datepointer) and self.time_match(self.datepointer):
                return self.datepointer

        # None found, find the next day it fires
        for x in range(365 * 100):
            if self.date_match(self.datepointer):
                break
            self.datepointer += timedelta(days = 1)

        if x == 365 * 100:
            return None

        # Find the time it fires on that day
        for x in range(60 * 24):
            self.datepointer += timedelta(minutes = 1)
            if self.time_match(self.datepointer):
                return self.datepointer

    def previous(self):
        """
        the last date at which this cron fired
        returns None if it didn't in the last 100 years
        """
        for x in range(365 * 100):
            if self.date_match(self.datepointer):
                break
            self.datepointer -= timedelta(days = 1)
        for x in range(60 * 24):
            if self.time_match(self.datepointer):
                break
            self.datepointer -= timedelta(minutes = 1)
        return self.datepointer

    def occurs_between(self, date1, date2):
        """
        Will this cron fire between date 1 and date 2?
        If so, return the exact time(s) it does.
        Useful for a daily or weekly overview
        """
        self.datepointer = date1
        d = self.next()
        while d < date2:
            yield d
            d = self.next()

    def _parse_cron(self):
        result = {}
        order = ['minute', 'hour', 'day', 'month', 'weekday', 'year']
        return {order[i] : self._getrange(tab, order[i]) for i, tab in enumerate(self.cron.split())}

    def _getrange(self, tab, type):
        ranges = {
            'minute' : (60,),
            'hour' : (24,),
            'day' : (1,32),
            'month' : (1,13),
            'weekday' : (7,),
            'year' : (1970,3000)
            }
        if tab.isdigit():
            return [int(tab)]
        elif "-" in tab:
            start, finish = tab.split("-")
            finish = finish.split("/")[0]
            result = range(int(start), int(finish))
        elif "*" in tab:
            result = range(*ranges[type])
        else:
            if "," in tab:
                result = []
                [result.extend(self._getrange(bit, type)) for bit in tab.split(",")]
            else:
                raise ValueError("Unable to parse this bit: {}".format(tab))

        if "/" in tab:
            interval = int(tab.split("/")[1])
            result = result[::interval]

        return result
            
        
                                                       


