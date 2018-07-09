# Sometimes you need various information about the event that caused the script to trigger.
# This scripts demonstrates how to retrieve various event information using lucid.
#
# Please see: https://github.com/OH-Jython-Scripters/lucid/blob/master/README.md
#

from lucid.rules import rule, addRule
from lucid.triggers import ItemStateUpdateTrigger, CronTrigger
from lucid.utils import getEvent

@rule
class ShowSomeEventInfo(object):
    def getEventTriggers(self):
        return [
            ItemStateUpdateTrigger('Button_Box_Sw_4'),
            CronTrigger('0 0/1 * 1/1 * ? *'), # Runs every minute
        ]

    def execute(self, modules, inputs):
        self.log.setLevel(DEBUG)
        event = getEvent(inputs)
        if event.isItem:
            self.log.debug('Triggering item name: \'' + unicode(event.itemName) + '\', state: ' + str(event.state))
            item = event.item # Get the item object for item that caused the event
            self.log.debug('item: ' + unicode(item.name) + ' isActive(): ' + str(event.isActive))
            self.log.debug('item: ' + unicode(item.name) + ' has a new state: ' + str(item.state))
        self.log.debug('event type: ' + event.type)
        self.log.debug('This was a cron event: ' + str(event.isCron))
        self.log.debug('This was a command event: ' + str(event.isCommand))
        self.log.debug('This was an update event: ' + str(event.isUpdate))

addRule(ShowSomeEventInfo())
