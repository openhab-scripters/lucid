from lucid.rules import rule, addRule
from lucid.triggers import CronTrigger

@rule
class HelloWorld(object):
    def getEventTriggers(self):
        return [
            CronTrigger('0 0/1 * 1/1 * ? *'), # Runs every minute
        ]

    def execute(self, modules, inputs):
        self.log.info('Hello world from lucid!')

addRule(HelloWorld())
