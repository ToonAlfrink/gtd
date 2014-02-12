"""Process inbox items one by one"""
from time import sleep
from gtd.actions.models import Item, NextAction, DeadlineAction, WaitingFor, Project
from gtd.tools import inp
from gtd.actions.add import add_action_cli, create_action

class ProcessScript(object):
    def run(self):
        print("Good day")
        sleep(1)
        self._iteritems()
        print("Done. Cheers!")
        
    def _iteritems(self):
        items = Item.objects.filter(filed = False)
        print("You have {n} items in your inbox".format(n = items.count()))
        for item in items:
            while True:
                try:
                    add_action_cli(item)
                except KeyboardInterrupt:
                    cont = raw_input("Start over from last item? (RET/^C)\n> ")
                else:
                    more = inp("Continue? (y/n)", ['x == "y" or x == "n"'])
                    if more == 'n':
                        break
                        
            if not item.filed:
                item.delete()

if __name__ == "__main__":
    p = ProcessScript()
    p.run()
