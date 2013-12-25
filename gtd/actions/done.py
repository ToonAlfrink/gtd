"""Mark an action as completed"""

from gtd.actions.models import WaitingFor, NextAction, SomeDayAction
#from gtd.calendar.models import CalendarAction

class DoneScript:
    def run(self, opts):
        try:
            action = self._parseopts(opts)
        except Exception:
            print("gtd done [-n|-w|-s|-d] [id]")
            return
        action.done = True
        action.save()
        self._reward()
        
    def _parseopts(self, opts):
        type = opts[0]
        pk = int(opts[1])
        if type == "-n":
            return NextAction.objects.get(pk = pk)
        elif type == "-w":
            return WaitingFor.objects.get(pk = pk)
        elif type == "-s":
            return SomeDayAction.objects.get(pk = pk)
        elif type == "-c":
            #return CalendarAction.objects.get(pk = pk)
            pass
        else:
            print("invalid type")

    def _reward(self):
        """Do something to reward the user"""
        print("You da man, man.")


if __name__ == "__main__":
    from sys import argv
    d = DoneScript()
    d.run(argv[1:])
