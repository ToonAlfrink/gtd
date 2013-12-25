"""Add an action straight from the cli"""

from time import sleep
from gtd.actions.models import WaitingFor, NextAction, SomeDayAction, Project, DeadlineAction, RecurrentAction
from gtd.tools import inp

def create_action(type = None):
    if not type:
        type = inp("[n] = next action | [w] = waiting for | [s] = some day/maybe | [d] = deadline | [r] = recurrent action", ['x in "nwsdr"'])
    if type == "n":
        action = NextAction.create_cli()
    elif type == "w":
        action = WaitingFor.create_cli()
    elif type == "s":
        action = SomeDayAction.create_cli()
    elif type == "d":
        action = DeadlineAction.create_cli()
    elif type == "r":
        action = RecurrentAction.create_cli()
    action.save()

def add_actionable_cli():
    choice = inp("[e] = execute | [d] = delegate | [l] = list", ['x in "edl"'])
    if choice == "e":
        raw_input("Gogogo! 2 minutes! [RET]\n> ")
        print("Win.")
    elif choice == "d":
        raw_input("Delegate that shit! [RET]\n> ")
        waiting = inp("Would you like to create a waiting-for action? (y/n)", ['x in "yn"'])
        if waiting == "y":
            create_action(type = 'w')
    elif choice == "l":
        create_action()

def add_action_cli(item = None):
    if item:
        print(item.info)
        choice = inp("[p] = project | [f] = file | [a] = actionable | [d] = delete", ['x in "pfad" and len(x) == 1'])
    else:
        choice = inp("[p] = project | [a] = actionable", ["x == 'p' or x == 'a'"])
    if choice == "p":
        Project.create_cli()
    elif choice == "f":
        item.filed = True
        item.save()
    elif choice == "a":
        add_actionable_cli()
    elif choice == "d":
        item.delete()
    print("That's it for this item.")
    sleep(1)


if __name__ == "__main__":
    add_action_cli()
