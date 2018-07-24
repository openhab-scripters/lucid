# The lucid step_by_step script will take you through some very basic steps using lucid and Jython
# This is the starting script and we will slowly add some complicity.

from lucid.rules import rule, addRule # Needed for defining and adding a rule
from lucid.triggers import ItemStateChangeTrigger # Import the different type of triggers that you will be using

# First we add a rule that triggers upon the change of any of 2 switches.
# To run this, you need to define 2 openHAB switch items and name them "My_TestSwitch_1" and "My_TestSwitch_2"
# Add them to a site map so that you can operate them and watch the debug output.
# You will find that the script won't trigger when My_TestSwitch_2 when changes from ON to OFF

@rule
class StepByStep(object): # Giving the class a unique name
    def getEventTriggers(self):
        return [
            ItemStateChangeTrigger('My_TestSwitch_1'), # Triggering when the switch changes its state.
            ItemStateChangeTrigger('My_TestSwitch_2', ON), # Only trigger when switch turns on
        ]

    def execute(self, modules, inputs):
        self.log.info('One of the test switches has changed its state') # That's all we do

addRule(StepByStep()) # Needed to add the rule, use the same name as defined for the class
