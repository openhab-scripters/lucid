# This example scripts demonstrates how you can use lucid for reading
# various configuration entries that you have stored in the
# lucid configuration file.
#
# Q: Why would I want to do something like that?
# A: Jython scripts using lucid sometimes need a place to store various settings
# like a username, an application-ID, an update frequency etc. Those settings
# could be entered as constants directly in the main script but that makes it
# difficult to share them with other fellow Jython scripters and it's easy to
# accidentally overwrite the configuration data when downloading an updated script.
# Therefore lucid provides a module for storing this configuration data as
# demonstrated below.
#
# This configuration file is not restricted to "official" lucid scripts. That is,
# you might probably wan't to use it for your own personal scripts too!

# Unless you already have a lucid config file, please have a look at
# https://github.com/OH-Jython-Scripters/lucid#configuration-file for
# how to make one.
#
# This example script is reading a dictionary named "wunderground" as seen in
# the example config file: https://github.com/OH-Jython-Scripters/lucid/blob/master/automation/lib/python/lucid/example_config.py
# Add entries to the config file using your favorite editor.
# The syntax for the configuration file is pure python 2.7. 

from lucid.rules import rule, addRule
from lucid.triggers import CronTrigger
import lucid.config as config
from logging import DEBUG, INFO, WARNING, ERROR

@rule
class readConfigExample(object):
    def getEventTriggers(self):
        return [CronTrigger('0 0/1 * 1/1 * ? *')] # Runs every minute
    def execute(self, modules, inputs):

        self.log.setLevel(DEBUG) # Set the logging level to DEBUG

        # Get a single value:
        sonsorName = config.wunderground['sensors']['tempc']
        self.log.debug('Read sensorname from the lucid config file: ' + sonsorName)

        # wunderground['sensors'] is a dictionary. Let's iterate through it
        self.log.debug('Iterate through a dictionary in the lucid configuration file')
        for the_key, the_value in config.wunderground['sensors'].iteritems():
            self.log.debug('Key: ' + the_key + ', Value: ' + the_value)

addRule(readConfigExample())
