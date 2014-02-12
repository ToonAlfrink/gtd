"""GTD Review"""
from time import sleep
from datetime import date, timedelta

from gtd.actions.models import Project, NextAction, WaitingFor, SomeDayAction
from gtd.actions.process import ProcessScript
from gtd.actions.week import week
from gtd.actions.add import create_action
from gtd.tools import inp


class ReviewScript(object):
    def run(self):
        #check heap
        #ProcessScript().run()
        #check gmail
        #inp("Go check your gmail, now!")
        #check last week
        #self.checkweek(date.today() - timedelta(days = 7))
        #check next week
        #self.checkweek(date.today())
        #check projects
        self.checkprojects()
        #check actions
        self.checkactions(NextAction)
        #check waiting-fors
        self.checkactions(WaitingFor)
        #check someday-maybes
        self.checkactions(SomeDayAction)
        #brainstorm actions
        self.brainstorm()
        #check next-actions on projects
        self.checkprojectnext()

    def checkweek(self, day):
        week(day)
        add = inp("Anything to add? [y/n]", ['x in "yn"'])
        while add == 'y':
            create_action()
            add = inp("Anything to add? [y/n]", ['x in "yn"'])

    def checkprojects(self):
        for p in Project.objects.filter():
            n_nextactions = NextAction.objects.filter(project=p.id, done=False).count()
            n_waiting = WaitingFor.objects.filter(project=p.id,done=False).count()
            keep = inp("{p.name} ({n_nextactions} actions, waiting for {n_waiting})\nKeep? [y/n]".format(**locals()),['x in "yn"'])
            if keep == 'n':
                sure = inp("Sure? [Y/n]")
                if sure == 'Y':
                    p.delete()

    def checkactions(self, model):
        for a in model.objects.filter(done=False):
            print(a.project and a.project.name)
            print(a.name)
            do = inp("[c = complete | d = delete | k = keep]",['x in "cdk"','len(x)==1'])
            if do == 'c':
                a.done = True
                a.save()
            elif do == 'd':
                a.delete()

    def brainstorm(self):
        add = inp("Would you like to add any actions you can think of now? [y/n]",["x in 'yn'"])
        while add == 'y':
            create_action()
            add = inp("Anything else? [y/n]",["x in 'yn'"])

    def checkprojectnext(self):
        for p in Project.objects.all():
            actions = NextAction.objects.filter(project = p.id).count()
            subprojects = Project.objects.filter(parent = p.id).count()
            if not (actions or subprojects):
                print("{p.name} lacks a next action or subproject.".format(**locals()))
                add_action_cli()


if __name__ == "__main__":
    r = ReviewScript()
    r.run()
