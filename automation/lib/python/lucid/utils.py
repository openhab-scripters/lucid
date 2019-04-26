# -*- coding: utf-8 -*-
from org.eclipse.smarthome.core.types import UnDefType
from org.eclipse.smarthome.core.library.types import IncreaseDecreaseType, NextPreviousType, OnOffType, OpenClosedType, PlayPauseType, RewindFastforwardType, StopMoveType, UpDownType, DecimalType
import org.joda.time.DateTime as DateTime
from org.joda.time.format import DateTimeFormat
from lucid.log import logging, LOG_PREFIX
import lucid.config as config
log = logging.getLogger(LOG_PREFIX + '.utils')
import random
import time

# Get direct access to the JSR223 scope types and objects (for Jython modules imported into scripts)
from lucid.jsr223.scope import events, itemRegistry

# Some useful dictionaries
PRIO = {'LOW': 0, 'MODERATE': 1, 'HIGH': 2, 'EMERGENCY': 3}
LUX_LEVEL = {'BLACK': 4, 'DARK': 60, 'SHADY': 380}
LIGHT_LEVEL = {'BLACK': 0, 'DARK': 1, 'SHADY': 2, 'BRIGHT': 3}
PUSHOVER_PRIO = {'LOWEST': -2, 'LOW': -1, 'NORMAL': 0, 'HIGH': 1, 'EMERGENCY': 2}
MODE = {'OFF': 0, 'ON': 1}
LIGHTING_THEME = {'OFF': 0, 'NORMAL': 1, 'MOVIE': 2, 'DINNER': 3, 'PARTY': 4, 'ALERT': 99}
SOLARTIME = {'NIGHT': 0, 'DAWN': 1, 'DAY': 2, 'DUSK': 3} # Solar based
TIMEOFDAY = {'NIGHT': 0, 'MORNING': 1, 'DAY': 2, 'EVENING': 3} # Regardless of the sun
WIND_SPEEDS = {'CALM_TO_LIGHT_BREEZE': 3.4, 'GENTLE_BREEZE': 5.5, 'MODERATE_BREEZE': 8.0, 'FRESH_BREEZE': 10.8, 'STRONG_BREEZE': 13.9, 'MODERATE_GALE': 17.2, 'FRESH_GALE': 20.8, 'STRONG_GALE': 24.5, 'STORM': 28.5, 'VIOLENT_STORM': 32.7, 'HURRICANE': 999.9}
WIND_TEXTS = {0: u'Calm to light breeze. 0–3,3 m/s', 1: u'Gentle breeze. 3,4–5,4 m/s', 2: u'Moderate breeze. 5,5–7,9 m/s', 3: u'Fresh breeze. 8,0–10,7 m/s', 4: u'Strong breeze. 10,8–13,8 m/s', 5: u'Moderate gale. 13,9–17,1 m/s', 6: u'Fresh gale. 17,2–20,7 m/s', 7: u'Strong gale. 20,8–24,4 m/s', 8: u'Storm. 24,5–28,4 m/s', 9: u'Violent storm. 28,5–32,6 m/s', 10: u'Hurricane. Mer än 32,6 m/s'}

# Some useful constants
PUSHOVER_DEF_DEV = "d5833"

NULL = UnDefType.NULL
UNDEF = UnDefType.UNDEF
ON = OnOffType.ON
OFF = OnOffType.OFF
OPEN = OpenClosedType.OPEN
CLOSED = OpenClosedType.CLOSED

def isActive(item):
    '''
    Tries to determine if a device is active (tripped) from the perspective of an alarm system.
    A door lock is special in the way that when it's locked its contacts are OPEN hence
    the value needs to be inverted for the alarm system to determine if it's 'active'
    '''
    active = False
    if item.state in [ON, OPEN]:
        active = True
    active = not active if config.customGroupNames['lockDevice'] in item.groupNames else active
    return active

def curDateText():
    '''Get the current date and time as text'''
    return str(DateTimeFormat.forPattern("yyyy-MM-dd HH:mm:ss").print(DateTime.now()))

def kw(dict, search):
    '''Get key by value in dictionary'''
    for k, v in dict.iteritems():
        if v == search:
            return k

def iround(x):
    """iround(number) -> integer. Round a float to the nearest integer."""
    y = round(x) - .5
    return int(y) + (y > 0)

def getItemValue(itemName, defVal):
    '''
    Returns the items value if the item is initialized otherwise return the default value.
    itemRegistry.getItem will return an object also for uninitialized items but it has less methods.
    '''
    item = itemRegistry.getItem(itemName)
    if type(defVal) is int:
        return item.state.intValue() if item.state not in [NULL, UNDEF] else defVal
    elif type(defVal) is float:
        return item.state.floatValue() if item.state not in [NULL, UNDEF] else defVal
    elif defVal in [ON, OFF, OPEN, CLOSED]:
        return item.state if item.state not in [NULL, UNDEF] else defVal
    elif type(defVal) is str:
        return item.state.toFullString() if item.state not in [NULL, UNDEF] else defVal
    elif type(defVal) is DateTime:
        # We return a to a org.joda.time.DateTime from a org.eclipse.smarthome.core.library.types.DateTimeType
        return DateTime(item.state.calendar.timeInMillis) if item.state not in [NULL, UNDEF] else defVal
    else:
        log.error('The type of the passed default value is not handled')
        return None

def getLastUpdate(pe, item):
    '''
    Returns the items last update datetime as a 'org.joda.time.DateTime',
    http://joda-time.sourceforge.net/apidocs/org/joda/time/DateTime.html
    '''
    try:
        if pe.lastUpdate(item) is None:
            log.warning('No existing lastUpdate data for item: ' + unicode(item.name) + ', returning 1970-01-01T00:00:00Z')
            return DateTime(0)
        return pe.lastUpdate(item).toDateTime()
    except:
        # I have an issue with OH file changes being detected (StartupTrigger only) before the file
        # is completely written. The first read breaks because of a partial file write and the second read succeeds.
        log.warning('Exception when getting lastUpdate data for item: ' + unicode(item.name) + ', returning 1970-01-01T00:00:00Z')
        return DateTime(0)

def sendCommand(itemName, newValue):
    '''
    Sends a command to an item regerdless of it's current state
    '''
    events.sendCommand(itemName, str(newValue))

def postUpdate(itemName, newValue):
    '''
    Posts an update to an item regerdless of it's current state
    '''
    events.postUpdate(itemName, str(newValue))

def postUpdateCheckFirst(itemName, newValue, sendACommand=False, floatPrecision=-1):
    '''
    newValue must be of a type supported by the item

    Checks if the current state of the item is different than the desired new state.
    If the target state is the same, no update is posted.
    sendCommand vs postUpdate:
    If you want to tell something to change, (turn a light on, change the thermostat
    to a new temperature, start raising the blinds, etc.), then you want to send
    a command to an item using sendCommand.
    If your items' states are not being updated by a binding, the autoupdate feature
    or something else external, you will probably want to update the state in a rule
    using postUpdate.
    '''
    compareValue = None
    item = itemRegistry.getItem(itemName)

    if item.state not in [NULL, UNDEF]:
        if type(newValue) is int:
            compareValue = itemRegistry.getItem(itemName).state.intValue()
        elif type(newValue) is float:
            '''
            Unfortunately, most decimal fractions cannot be represented exactly as binary fractions.
            A consequence is that, in general, the decimal floating-point numbers you enter are only
            approximated by the binary floating-point numbers actually stored in the machine.
            Therefore, comparing the stored value with the new value will most likely always result in a difference.
            You can supply the named argument floatPrecision to round the value before comparing
            '''
            if floatPrecision == -1:
                compareValue = itemRegistry.getItem(itemName).state.floatValue()
            else:
                compareValue = round(itemRegistry.getItem(itemName).state.floatValue(), floatPrecision)
        elif newValue in [ON, OFF, OPEN, CLOSED]:
            compareValue = itemRegistry.getItem(itemName).state
        elif type(newValue) is str:
            compareValue = itemRegistry.getItem(itemName).state.toString()
        else:
            log.error('Can not set '+str(itemName)+' to the unsupported type '+str(type(newValue))+'. Value: '+str(newValue))
    if (compareValue is not None and compareValue != newValue) or item.state in [NULL, UNDEF]:
        if sendACommand:
            log.debug('New sendCommand value for '+itemName+' is '+str(newValue))
            sendCommand(itemName, newValue)
        else:
            log.debug('New postUpdate value for '+itemName+' is '+str(newValue))
            postUpdate(itemName, newValue)
        return True
    else:
        return False

def sendCommandCheckFirst(itemName, newValue, floatPrecision=-1):
    ''' See postUpdateCheckFirst '''
    return postUpdateCheckFirst(itemName, newValue, sendACommand=True, floatPrecision=floatPrecision)

def hasReloadFinished(exitScript=False):
    '''
    Sometimes scripts are running before all Items have finished loading.
    To prevent that, place an item, only for this purpose last in your last items file.(alphabetic order).
    The item must be persisted on change.
    We will check if this item has a specific value. Define the name of the item in your lucid config file.
    Name it whatever you like but it's better if it starts with the last letter in the alphabet.
    Example Item:
    String ZZZ_Test_Reload_Finished (G_PersistOnChange)
    '''
    HELLO = 'Hello'
    try:
        if itemRegistry.getItem(config.customItemNames['reloadFinished']).state.toString == HELLO:
            return True
    except:
        if exitScript: return False
        timeToSleep = 0.5+random.uniform(0, 1)
        time.sleep(timeToSleep)
        log.info('WAITING '+str(timeToSleep)+' sec !!!')
        postUpdateCheckFirst(config.customItemNames['reloadFinished'], HELLO)
    return True

def pronounce(word):
    '''Makes a word easier to pronounce for TTS'''
    if word in config.pronounce:
        return config.pronounce[word]
    else:
        return word

def greeting():
    # To use this, you should set up astro.py as described
    # here https://github.com/OH-Jython-Scripters/lucid/blob/master/Script%20Examples/astro.py
    # It will take care of updating the item 'V_TimeOfDay' for you
    timeOfDay = getItemValue('V_TimeOfDay', TIMEOFDAY['DAY'])
    if timeOfDay in config.greeting:
        return config.greeting[timeOfDay]
    else:
        return 'good day'

def isBright():
    '''Returns true when light level is bright'''
    return getItemValue(config.customItemNames['sysLightLevel'], LIGHT_LEVEL['BRIGHT']) == LIGHT_LEVEL['BRIGHT']

def isShady():
    '''Returns true when shady or darker than shady'''
    return getItemValue(config.customItemNames['sysLightLevel'], LIGHT_LEVEL['BRIGHT']) <= LIGHT_LEVEL['SHADY']

def isDark():
    '''Returns true when dark or darker than dark'''
    return getItemValue(config.customItemNames['sysLightLevel'], LIGHT_LEVEL['BRIGHT']) <= LIGHT_LEVEL['DARK']

def isBlack():
    '''Returns true if black, otherwise false'''
    return getItemValue(config.customItemNames['sysLightLevel'], LIGHT_LEVEL['BRIGHT']) <= LIGHT_LEVEL['BLACK']

'''
				 Safety pig has arrived!
				
				  _._ _..._ .-',     _.._(`))
				 '-. `     '  /-._.-'    ',/
				    )         \            '.
				   / _    _    |             \
				  |  a    a    /              |
				  \   .-.                     ;  
				   '-('' ).-'       ,'       ;
				      '-;           |      .'
				         \           \    /
				         | 7  .__  _.-\   \
				         | |  |  ``/  /`  /
				        /,_|  |   /,_/   /
				           /,_/      '`-'
'''
