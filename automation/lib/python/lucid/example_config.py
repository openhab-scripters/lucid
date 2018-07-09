# -*- coding: utf-8 -*-
# lucid config file
# Note! If you make any changes to this file, your script must reload this library

# Rename this file to config.py and edit it to suit your needs

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
pronounce = {
    'Carlos': 'Carl'
}
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
