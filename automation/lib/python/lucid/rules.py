import functools
from java.util import UUID
from org.eclipse.smarthome.automation import Rule as SmarthomeRule
from org.eclipse.smarthome.core.types import UnDefType
from org.eclipse.smarthome.core.library.types import IncreaseDecreaseType, NextPreviousType, OnOffType, OpenClosedType, PlayPauseType, RewindFastforwardType, StopMoveType, UpDownType, DecimalType

from lucid.log import logging, log_traceback, LOG_PREFIX
from logging import DEBUG, INFO, WARNING, ERROR

import lucid.config as config

from lucid.jsr223 import scope, get_automation_manager
from lucid.jsr223.scope import events, itemRegistry
import random
import time

NULL = UnDefType.NULL
UNDEF = UnDefType.UNDEF
ON = OnOffType.ON
OFF = OnOffType.OFF
OPEN = OpenClosedType.OPEN
CLOSED = OpenClosedType.CLOSED

scope.scriptExtension.importPreset("RuleSimple")

def set_uid_prefix(rule, prefix=None):
    if prefix is None:
        prefix = type(rule).__name__
    uid_field = type(SmarthomeRule).getClass(SmarthomeRule).getDeclaredField(SmarthomeRule, "uid")
    uid_field.setAccessible(True)
    uid_field.set(rule, "{}-{}".format(prefix, str(UUID.randomUUID())))

def isActive(item):
    '''
    Tries to determine if a device is active (tripped) from the perspective of an alarm system.
    A door lock is special in the way that when it's locked its contacts are OPEN hence
    the value needs to be inverted for the alarm system to determine if it's 'active'
    '''
    active = False
    if item.state in [ON, OPEN]:
        active = True
    active = not active if 'G_Lock' in item.groupNames else active
    return active

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
        logging.info('WAITING '+str(timeToSleep)+' sec !!!')
        events.postUpdate(config.customItemNames['reloadFinished'], HELLO)
    return True

class Event:
    def __init__(self, inputs):
        self.isCron = False
        self.isStartup = False
        self.isCommand = False
        self.isUpdate = False
        self.itemName = None
        self.state = None
        self.isActive = None
        self.item = None
        self.isItem = False
        if not inputs:
            self.type = 'Cron'
            self.isCron = True
        elif 'event' in inputs:
            # Type can be 'ItemStateEvent', 'ItemStateChangedEvent' or 'ItemCommandEvent'
            self.type = inputs['event'].getType()
        else:
            self.type = 'Startup'
            self.isStartup = True
        _event = inputs.get('event')
        if _event is not None:
            self.itemName = _event.itemName
            if 'getItemState' in dir(_event):
                _state = _event.getItemState()
                _oldState = _event.getOldItemState() if 'getOldItemState' in dir(_event) else None
                self.isUpdate = True
            elif 'getItemCommand' in dir(_event):
                _state = _event.getItemCommand()
                _oldState = None # object has no attribute 'getOldItemCommand'
                self.isCommand = True
            _attr = getattr(_state, 'intValue', None)
            _oldAttr = getattr(_oldState, 'intValue', None)
            if type(_state) in [IncreaseDecreaseType, NextPreviousType, OnOffType, OpenClosedType, PlayPauseType, RewindFastforwardType, StopMoveType, UpDownType]:
                self.state = _state.toString()
            elif _attr is not None:
                self.state = _state.floatValue() if '.' in str(_state) else _state.intValue()
            elif str(type(_state)) == 'NoneType':
                self.state = None
            else:
                self.state = _state.toString()
            if type(_oldState) in [IncreaseDecreaseType, NextPreviousType, OnOffType, OpenClosedType, PlayPauseType, RewindFastforwardType, StopMoveType, UpDownType]:
                self.oldState = _oldState.toString()
            elif _oldAttr is not None:
                self.oldState = _oldState.floatValue() if '.' in str(_oldState) else _oldState.intValue()
            elif str(type(_oldState)) == 'NoneType' or _oldState is None:
                self.oldState = None
            else:
                self.oldState = _oldState.toString()
            self.item = itemRegistry.getItem(self.itemName)
            self.isActive = isActive(self.item)
            self.isItem = True

def wrap_execute(fn):
    """Wrapper to extend the execute function"""
    functools.wraps(fn)
    def wrapper(self, modules, inputs):
        hasReloadFinished()
        self.event = Event(inputs)

        # Add global names, using the function's own global namespace:
        g = fn.__globals__
        g['DEBUG'] = DEBUG
        g['INFO'] = INFO
        g['WARNING'] = WARNING
        g['ERROR'] = ERROR
        g['NULL'] = NULL
        g['UNDEF'] = UNDEF
        g['ON'] = ON
        g['OFF'] = OFF
        g['OPEN'] = OPEN
        g['CLOSED'] = CLOSED

        fn(self, modules, inputs)
        # Place to add stuff after wrapped function
    return wrapper

def wrap_getEventTriggers(fn):
    """Wrapper to extend the getEventTriggers function"""
    functools.wraps(fn)
    def wrapper():
        # Add global names, using the function's own global namespace:
        g = fn.__globals__
        g['NULL'] = str(NULL)
        g['UNDEF'] = str(UNDEF)
        g['ON'] = str(ON)
        g['OFF'] = str(OFF)
        g['OPEN'] = str(OPEN)
        g['CLOSED'] = str(CLOSED)
        g['EVERY_10_SECONDS'] = str(int(round(0.5+random.uniform(1, 9))))+"/10 * * * * ?"
        g['EVERY_15_SECONDS'] = str(int(round(0.5+random.uniform(1, 14))))+"/15 * * * * ?"
        g['EVERY_30_SECONDS'] = str(int(round(0.5+random.uniform(1, 29))))+"/30 * * * * ?"
        g['EVERY_MINUTE'] = str(int(round(0.5+random.uniform(3, 57))))+" 0/1 * 1/1 * ? *"
        g['EVERY_OTHER_MINUTE'] = str(int(round(0.5+random.uniform(3, 57))))+" 0/2 * 1/1 * ? *"
        g['EVERY_5_MINUTES'] = str(int(round(0.5+random.uniform(3, 57))))+" "+str(int(round(0.5+random.uniform(1, 9))))+"/5 * 1/1 * ? *"
        g['EVERY_10_MINUTES'] = str(int(round(0.5+random.uniform(3, 57))))+" "+str(int(round(0.5+random.uniform(1, 9))))+"/10 * 1/1 * ? *"
        g['EVERY_15_MINUTES'] = str(int(round(0.5+random.uniform(3, 57))))+" "+str(int(round(0.5+random.uniform(1, 9))))+"/15 * 1/1 * ? *"
        g['EVERY_30_MINUTES'] = str(int(round(0.5+random.uniform(3, 57))))+" "+str(int(round(0.5+random.uniform(1, 29))))+"/30 * 1/1 * ? *"
        g['EVERY_HOUR'] = str(int(round(0.5+random.uniform(3, 57))))+" "+str(int(round(0.5+random.uniform(3, 57))))+" 0/1 1/1 * ? *"
        g['EVERY_6_HOURS'] = str(int(round(0.5+random.uniform(3, 57))))+" "+str(int(round(0.5+random.uniform(3, 57))))+" 0/6 1/1 * ? *"
        g['EVERY_DAY_AROUND_NOON'] = str(int(round(0.5+random.uniform(3, 57))))+" "+str(int(round(0.5+random.uniform(3, 57))))+" 12 1/1 * ? *"

        return fn()
    return wrapper

def rule(clazz):
    def init(self, *args, **kwargs):
        scope.SimpleRule.__init__(self)
        set_uid_prefix(self)
        self.log = logging.getLogger(LOG_PREFIX + "." + clazz.__name__)
        self.DEBUG = DEBUG
        self.INFO = INFO
        self.WARNING = WARNING
        self.ERROR = ERROR
        self.config = config
        clazz.__init__(self, *args, **kwargs)
        if self.description is None and clazz.__doc__:
            self.description = clazz.__doc__
        if hasattr(self, "getEventTriggers"):
            self.triggers = log_traceback(wrap_getEventTriggers(self.getEventTriggers))()
        elif hasattr(self, "getEventTrigger"):
            # For OH1 compatibility
            self.triggers = log_traceback(wrap_getEventTriggers(self.getEventTrigger))()
    subclass = type(clazz.__name__, (clazz, scope.SimpleRule), dict(__init__=init))
    subclass.execute = log_traceback(wrap_execute(clazz.execute))
    return subclass

def addRule(rule):
    get_automation_manager().addRule(rule)
