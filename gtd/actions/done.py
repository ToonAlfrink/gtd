"""Mark an action as completed"""

from gtd.actions.models import WaitingFor, NextAction, SomeDayAction, DeadlineAction, RecurrentAction
from datetime import datetime, timedelta
import pytz

class DoneScript:
    def run(self, opts):
        action = self._parseopts(opts)
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
        elif type == "-d":
            return DeadlineAction.objects.get(pk = pk)
        elif type == "-r":
            action = RecurrentAction.objects.get(pk = pk)
            action.complete()
            return action
        else:
            raise ValueError("invalid type")

    def _reward(self):
        """Do something to reward the user"""
        print("You da man, man.")


if __name__ == "__main__":
    from sys import argv
    d = DoneScript()
    d.run(argv[1:])
