# -*- coding: utf-8 -*-
'''
lucid config file
Note! If you make any changes to this file, your script must reload this library
See: https://github.com/OH-Jython-Scripters/lucid#loading-and-reloading-the-jython-rule-binding

Rename this file to config.py and edit it to suit your needs

Some configuration items are mandatory, hence you should not remove them.
'''
from logging import DEBUG, INFO, WARNING, ERROR

# Define at what time of day you want morning, day,evening and night to start
# Mandatory. Do not remove.
timeOfDay = {
    'morningStart': {'Hour': 7, 'Minute': 0},
    'dayStart': {'Hour': 8, 'Minute': 0},
    'eveningStart': {'Hour': 18, 'Minute': 0},
    'nightStart': {'Hour': 22, 'Minute': 30}
}

# Mandatory. Do not remove.
customItemNames = {
    'sysLightLevel': 'Sys_LightLevel', # Item that holds daylight value in LUX
    'reloadFinished': 'ZZZ_Test_Reload_Finished', # A persisted item that we use to check if releoad has finished
    'allowTTSSwitch': 'Sonos_Allow_TTS_And_Sounds', # Switch item that must be ON to allow normal prio TTS and sounds to pass
}

# Mandatory. Do not remove.
customGroupNames = {
    'lockDevice': 'G_Lock', # Group Item name that you've assigned to all your door lock devices
}

autoremote = {
    'password': 'secret',
    'key': 'very-long-key-goes-here',
    }

clickatell = {
    'sender': '49123456789',
    'user': 'xxxxxxxxxxxx',
    'password': 'xxxxxxxxxxxxxxxxx',
    'apiid': 999999999999,
    'phonebook': {
        'Default': '49123456789',
        'Carl': '49987654321',
        'Betty': '4911111111',
    }
}

# Weather Underground Config
wunderground = {
    'logLevel': ERROR,
    'stationdata': {
        "weather_upload": True,
        "station_id": "XXXXXXX",
        "station_key": "xxxxxxxxxx",
        "upload_frequency": 5
    },
    'sensors': {
        "tempc": 'XXXXXXXXX',
        "humidity": 'XXXXXXXXX',
        "pressurembar": 'XXXXXXXXX',
        "soiltempc": 'XXXXXXXXX',
        "soilmoisture": 'XXXXXXXXX',
        "winddir": 'XXXXXXXXX',
        "windspeedms": 'XXXXXXXXX',
        "windgustms": 'XXXXXXXXX',
        "solarradiation": 'XXXXXXXXX'
    }
}

# Mandatory. Do not remove.
pronounce = {
    'Carlos': 'Carl'
}

# Mandatory. Do not remove.
greeting = {
    0: 'Good night',
    1: 'Good morning',
    2: 'Good day',
    3: 'Good evening'
}

sonos = {
    'rooms': {
        'Kitchen': {
            "name": 'Kitchen speaker',
            "audiosink": 'sonos:One:RINCON_999999999999999999',
            "defaultttsdevice": True,
            "volume": 40,
            "ttsvolume": 40,
            "ttslang": 'sv-SE',
            "ttsvoice": 'Astrid',
            "ttsengine": 'pollytts'
        },
        'Bedroom': {
            "name": 'Bedroom speaker',
            "audiosink": 'sonos:PLAY1:RINCON_999999999999999999',
            "defaultttsdevice": False,
            "volume": 40,
            "ttsvolume": 40,
            "ttslang": 'sv-SE',
            "ttsvoice": 'Astrid',
            "ttsengine": 'pollytts'
        },
    }
}
