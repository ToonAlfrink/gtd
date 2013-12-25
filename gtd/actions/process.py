"""Process inbox items one by one"""
from time import sleep
from gtd.actions.models import Item, NextAction, Project
from gtd.tools import inp
from gtd.actions.add import add_action_cli, create_action

class ProcessScript:
    def run(self):
        print("Good day")
        sleep(1)
        self._iteritems()
        print("That's it. Checking projects...")
        sleep(1)
        self._checkprojects()
        print("Done. Cheers!")
        
    def _iteritems(self):
        items = Item.objects.filter(filed = False)
        print("You have {n} items in your inbox".format(n = items.count()))
        for item in items:
            while True:
                try:
                    self._process(item)
                except KeyboardInterrupt:
                    cont = raw_input("Start over from last item? (RET/^C)\n> ")
                else:
                    more = inp("Continue? (y/n)", ['x == "y" or x == "n"'])
                    if more == 'n':
                        break
                        
            if not item.filed:
                item.delete()
                
                    
    def _process(self, item):
        add_action_cli(item)
            
    def _checkprojects(self):
        for project in Project.objects.all():
            if not any([project.id == p.parent_id for p in Project.objects.all()]):
                if not any([a.project_id == project.id for a in NextAction.objects.filter(done = False)]):
                    print("Project {project.pk}: '{project.name}' lacks a next action.".format(**locals()))
                    sleep(1)
                    create_action()


if __name__ == "__main__":
    p = ProcessScript()
    p.run()
