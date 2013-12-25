"""Script used to dump some piece of information, to be processed later"""
from __future__ import absolute_import

from time import sleep
from gtd.actions.models import Item

class CollectScript:
    def run(self):
        print("What's up!")
        sleep(1)
        item = Item()
        print("Write as much relevant info as possible")
        print("if done, write OK")
        item.info = ""
        while True:
            line = raw_input("> ")
            if line == "OK":
                break
            item.info += line + "\n"
        if item.info:
            item.info = item.info.strip()
            item.save()

if __name__ == "__main__":
    c = CollectScript()
    c.run()

    
