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


from datetime import datetime, timedelta
import pytz

class CronHandler(object):
    def __init__(self, cron):
        self.cron = cron

    def nextenabled(self):
        t = datetime.now(pytz.timezone('Europe/Amsterdam'))
        t -= timedelta(seconds = t.second)
        #check if it will ever enable
        parseorder = ['minute','hour','day','month','weekday','year']
        timedict = [(parseorder[i], _lis) for i, _lis in enumerate(self._parse())]

        maxdata = {}
        for unit in timedict:
            maxdata[unit[0]] = max(unit[1])
        month_maxday = self._maxday(maxdata['month'], maxdata['year'])
        if maxdata['day'] > month_maxday:
            maxdata['day'] = month_maxday

        maxdate = pytz.timezone('Europe/Amsterdam').localize(
            datetime(**{k : v for k, v in maxdata.items() if not k=='weekday'})
            )
        if maxdate < t:
            return None

        #get time of next occurrence
        for timeunit, _list in timedict[:2]:
            while True:
                if getattr(t, timeunit) in _list: 
                    break
                t += timedelta(**{timeunit + "s" : 1})

        #get day of next occurrence
        timedict = dict(timedict)
        while True:
            if t.year not in timedict['year'] or t.month not in timedict['month'] or t.day not in timedict['day'] or t.weekday() not in timedict['weekday']:
                pass
            else:
                break
            if t.year > max(timedict['year']):
                return None
            t += timedelta(days = 1)
        return t

    def _maxday(self, month, year):
        n_days_month = {
            1 : 31,2 : 28,3 : 31,4 : 30,
            5 : 31,6 : 30,7 : 31,8 : 31,
            9 : 30,10 : 31,11 : 30,12 : 31}
        if year % 4 == 0:
            n_days_month[2] = 29
        return n_days_month[month]

    def _firstenabled(self):
        data = self._parse()
        d = datetime(year = data[5][0],
                     month = data[3][0],
                     day = data[2][0],
                     hour = data[1][0],
                     minute = data[0][0])
        try:
            d = pytz.timezone('Europe/Amsterdam').localize(d)
        except OverflowError: #some silly date like 0000-00-00
            d = pytz.UTC.localize(d)
        return d

    def lastenabled(self):
        t = datetime.now(pytz.timezone('Europe/Amsterdam'))
        if self._firstenabled() > t: #hasn't been enabled yet
            return None
        #check if it will ever enable
        parseorder = ['minute','hour','day','month','weekday','year']
        timedict = [(parseorder[i], _lis) for i, _lis in enumerate(self._parse())]
        
        #get time of last occurrence
        for timeunit, _list in list(reversed(timedict))[4:]:
            while True:
                if getattr(t, timeunit) in _list: 
                    break
                t -= timedelta(**{timeunit + "s" : 1})
        #get day of last occurrence
        timedict = dict(timedict)
        while True:
            if t.year not in timedict['year'] or t.month not in timedict['month'] or t.day not in timedict['day'] or t.weekday() not in timedict['weekday']:
                pass
            else:
                break
            t -= timedelta(days = 1)
        return t

    def _parse(self, cron = None):
        if not cron:
            cron = self.cron
        result = []
        ranges = {0:(60,),1:(24,),2:(1,32),3:(1,13),4:(7,),5:(1,3000)}
        for i, tab in enumerate(cron.split()):
            if "-" in tab:
                start, finish = tab.split("-")
                result.append(range(int(start), int(finish)))
            elif "*" in tab:
                _list = range(*ranges[i])
                if "/" in tab:
                    interval = int(tab.split("/")[1])
                    _list = _list[::interval]
                result.append(_list)
            elif "," in tab:
                result.append([int(a) for a in tab.split(",")])
            elif tab.isdigit():
                result.append([int(tab)])
            else:
                raise ValueError("Can't parse this crontab: {tab}".format(**locals()))
        return result
