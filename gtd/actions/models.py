from django.db import models
from gtd.tools import inp, CronEntry
from datetime import datetime

class Item(models.Model):
    info = models.TextField()
    filed = models.BooleanField(default = False)

class Context(models.Model):
    name = models.CharField(max_length = 50)

    @classmethod
    def create(cls, name):
        print("creating context...")
        c = cls(name = name)
        return c

class Project(models.Model):
    name = models.CharField(max_length = 50)
    parent = models.ForeignKey('self', blank = True, null = True)

    @classmethod
    def get_cli(cls):
        for p in cls.objects.all():
            print(p.id, p.name)
        _id = inp("Select project (or type N)", ['x.isdigit() or x == "N"'])
        if not _id == "N":
            return cls.objects.get(pk = _id)

    @classmethod
    def create_cli(cls):
        project = cls()
        project.name = inp("Name?", ['len(x) > 3'])
        print("Now, please select a parent.")
        project.parent = cls.get_cli()
        project.save()
        return project

class Action(models.Model):
    name = models.CharField(max_length = 50)
    description = models.TextField()    
    done = models.BooleanField(default = False)
    project = models.ForeignKey(Project, blank = True, null = True)
    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_cli(cls):
        """Create item, using cli prompts"""
        action = cls()
        action.name = inp("Action name?", [])
        print("Please describe the action, type 'OK' if done.")
        lines = []
        while True:
            line = raw_input("> ")
            if line == "OK":
                break
            lines.append(line)
        action.description = "\n".join(lines)
        action.project = Project.get_cli()
        action = cls._create_cli(action)
        return action

    @classmethod
    def _create_cli(cls, action):
        return action

    class Meta:
        abstract = True

class WaitingFor(Action):
    pass
    
class NextAction(Action):
    context = models.ForeignKey(Context)
    duration = models.IntegerField()

    @classmethod
    def _create_cli(cls, action):
        for c in Context.objects.all():
            print(c.pk, c.name)
        choice = inp("Please choose a context or type ADD", ['x.isdigit() or x == "ADD"'])
        if choice == "ADD":
            name = inp("Name?")
            context = Context.create(name)
            context.save()
        elif choice.isdigit():
            context = Context.objects.get(pk = int(choice))
        action.context = context
        action.duration = inp("How long, in minutes, should this take?", ['x.isdigit()'])
        return action

class SomeDayAction(Action):
    pass

class DeadlineAction(NextAction):
    deadline = models.DateField()

    @classmethod
    def _create_cli(cls, action):
        action = NextAction._create_cli(action)
        action.deadline = inp("Deadline date?")
        return action

class RecurrentAction(Action):
    cron = models.CharField(max_length = 50)
    last_completed = models.DateTimeField(auto_now_add = True)
    duration = models.IntegerField()

    def __init__(self, *args, **kwargs):
        super(RecurrentAction, self).__init__(*args, **kwargs)
        self.cronhandler = CronEntry(self.cron)

    @classmethod
    def _create_cli(cls, action):
        action = Action._create_cli(action)
        action.cron = inp("Please input cron")
        return action

    def is_enabled(self):
        """Is this action to be done at the moment?"""
        l = self.last_completed
        p = self.cronhandler.previous()
        return self.last_completed < p

    def complete(self):
        self.last_completed = datetime.now()
        self.save()

