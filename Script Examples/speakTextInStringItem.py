from lucid.rules import rule, addRule
from lucid.triggers import ItemStateUpdateTrigger
from lucid.utils import getEvent
from lucid.speak import tts

@rule
class SpeakThisPhrase(object):
    """
    Make openHAB speak a message posting to the openHAB REST API from an external host
    This script watches an openHAB string item, e.g: String Speak_This "Speak this [%s]" <text> 
    Use curl from an external host to set the item to the text string that shall be spoken
    e.g. curl -X PUT --header "Content-Type: text/plain" --header "Accept: application/json" -d "Hello world" "http://OPENHABHOST:8080/rest/items/Speak_This/state"
    """
    def getEventTriggers(self):
        return [ItemStateUpdateTrigger('Speak_This')]
    def execute(self, modules, inputs):
        event = getEvent(inputs)
        tts(event.state)
addRule(SpeakThisPhrase())
