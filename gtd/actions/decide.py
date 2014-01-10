"""Pick out an action that, with the given context and time, is the best to do"""
from time import sleep
from random import random
from datetime import date, timedelta

from gtd.actions.models import Context, Project, NextAction, DeadlineAction, RecurrentAction
from gtd.tools import inp, CronEntry

class DecideScript:
    def run(self):
        action = self._recurrentaction() or self._deadlineaction() or self._nextaction()
        if action:
            self._printout(action)

    def _recurrentaction(self):
        print("Checking recurrent action...")
        for action in RecurrentAction.objects.all():
            if action.is_enabled():
                return action

    def _deadlineaction(self):
        print("Checking deadlineactions...")
        actions = DeadlineAction.objects.filter(done = False).order_by('deadline')
        for action in actions:
            if action.deadline < date.today() + timedelta(days = 7):
                return action
        

    def _nextaction(self):
        actions = NextAction.objects.filter(done = False)
        contexts = self._getcontexts()
        actions = actions.filter(context_id__in = contexts)
        n = actions.count()
        print("We have left, {n} next actions within context".format(**locals()))
        if n:
            sleep(1)
            if random() < .5:
                print("selecting randomly")
                action = actions.order_by('?')[0]
            else:
                print("selecting by add date")
                action = actions.order_by('created')[0]
            self._printout(action)

    def _getcontexts(self):
        for c in Context.objects.all():
            print(c.pk, c.name)
        contexts = inp("please choose contexts:", ['x.isdigit()'])
        return contexts
           
    def _printout(self, a):
        print("\n\n")
        if hasattr(a, 'project') and a.project:
            p = a.project
            projects = [a.project]
            while True:
                if hasattr(p, 'parent') and p.parent:
                    if not p.parent == p:
                        projects.append(p.parent)
                        p = p.parent
                    else:
                        print("recursive parent fail")
                        break
                else:
                    break
            for project in reversed(projects):
                print("-> " + project.name)
        
        print("{a.__class__.__name__} | {a.id} | {a.name}".format(**locals()))
        print("{a.description}".format(**locals()))
        if a.__class__ == DeadlineAction:
            print("Deadline: {a.deadline}".format(**locals()))
        print("\n")
 
if __name__ == "__main__":
    d = DecideScript()
    d.run()
