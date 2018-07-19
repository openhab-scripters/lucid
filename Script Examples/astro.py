'''
This script will calculate and save the "Time of day" and the "Solar time" of the day to items.
"Time of day" can be morning, day, evening or night. These are clock dependent.
"Solar time" can be dawn, day, dusk and night. These are dependent of the sun's position relative the horizon.

So depending on where you live and the season, the solar time might be "day" while time of day is "night"
and vice versa.

This topic by Rich Koshak might also be of interest: https://community.openhab.org/t/design-pattern-time-of-day/15407/4

Prerequisits:
=============================
- Astro binding installed.
- Download to openHAB maps directory: en_timeofday.map and en_solartime.map
  From https://github.com/OH-Jython-Scripters/lucid/tree/master/transform
- Persistence set up. The item group named G_PersistOnChange is persisted on change
- Items as defined below. 

Group G_PersistOnChange // Set up for persistence on change and system start up
Number V_SolarTime "Solar time of day [MAP(en_solartime.map):%s]" <sun> (G_PersistOnChange)
Number V_TimeOfDay "Time of day [MAP(en_timeofday.map):%s]" <sun> (G_PersistOnChange)
Number Sun_Position_Azimuth "Sun azimuth" <sun> {channel="astro:sun:local:position#azimuth"}
Number Sun_Position_Elevation "Sun elevation" <sun> {channel="astro:sun:local:position#elevation"}
DateTime V_CivilDawn "Civil Dawn [%1$tH:%1$tM]" <flow> (G_PersistOnChange) {channel="astro:sun:local:civilDawn#start"}
DateTime V_Sunrise "Sunrise [%1$tH:%1$tM]" <sun> (G_PersistOnChange) {channel="astro:sun:local:rise#start"}
DateTime V_Sunset "Sunset [%1$tH:%1$tM]" <sun> (G_PersistOnChange) {channel="astro:sun:local:set#start"}
DateTime V_CivilDuskStart "Civil dusk [%1$tH:%1$tM]" <flow> (G_PersistOnChange) {channel="astro:sun:local:civilDusk#start"}
DateTime V_CivilDuskEnd "Nautical dusk [%1$tH:%1$tM]" <moon> (G_PersistOnChange) {channel="astro:sun:local:civilDusk#end"}
'''

from logging import DEBUG, INFO, WARNING, ERROR
from lucid.rules import rule, addRule
from lucid.triggers import ChannelEventTrigger, StartupTrigger, CronTrigger
from lucid.utils import postUpdateCheckFirst, SOLARTIME, TIMEOFDAY, kw
import time
import org.joda.time.DateTime as DateTime

@rule
class TimeOfDayCalc(object):
    """Regardless of the sun, this rule determines what is day and night"""
    def getEventTriggers(self):
        return [
            CronTrigger('9 0 7 * * ?'), # E.g. 07:00:09 in morning
            CronTrigger('9 0 8 * * ?'),
            CronTrigger('9 0 18 * * ?'),
            CronTrigger('9 30 22 * * ?'),
            StartupTrigger()
        ]

    def execute(self, modules, inputs):
        #self.log.setLevel(INFO)
        self.log.setLevel(DEBUG)

        # Get the time period start times for today
        now = DateTime()
        morningStart = now.withTimeAtStartOfDay().plusHours(7).toInstant()
        dayStart = now.withTimeAtStartOfDay().plusHours(8).toInstant()
        eveningStart = now.withTimeAtStartOfDay().plusHours(18).toInstant()
        nightStart   = now.withTimeAtStartOfDay().plusHours(22).plusMinutes(30).toInstant()

        timeofday = TIMEOFDAY['NIGHT']
        if (now.isAfter(morningStart) and now.isBefore(dayStart)):
            timeofday = TIMEOFDAY['MORNING']
        elif (now.isAfter(dayStart) and now.isBefore(eveningStart)):
            timeofday = TIMEOFDAY['DAY']
        elif (now.isAfter(eveningStart) and now.isBefore(nightStart)):
            timeofday = TIMEOFDAY['EVENING']

        if postUpdateCheckFirst('V_TimeOfDay', timeofday):
            self.log.debug("Time of day now: " + kw(TIMEOFDAY, timeofday))

addRule(TimeOfDayCalc())

@rule
class AstroChannelRule(object):
    """This doc comment will become the ESH Rule documentation value for Paper UI"""
    def getEventTriggers(self):
        return [
            ChannelEventTrigger('astro:sun:local:civilDawn#event','START'),
            ChannelEventTrigger('astro:sun:local:rise#event','START'),
            ChannelEventTrigger('astro:sun:local:set#event','START'),
            ChannelEventTrigger('astro:sun:local:civilDusk#event','START'),
            ChannelEventTrigger('astro:sun:local:civilDusk#event','END'),
            StartupTrigger(),
        ]

    def execute(self, modules, inputs):
        #self.log.setLevel(INFO)
        self.log.setLevel(DEBUG)
        dawn_start = ir.get('V_CivilDawn').getState().calendar.timeInMillis
        day_start = ir.get('V_Sunrise').getState().calendar.timeInMillis
        dusk_start = ir.get('V_CivilDuskStart').getState().calendar.timeInMillis
        night_start = ir.get('V_CivilDuskEnd').getState().calendar.timeInMillis
        curr = None
        self.log.debug('dawn_start : ' + str(dawn_start))
        self.log.debug('day_start  : ' + str(day_start))
        self.log.debug('dusk_start : ' + str(dusk_start))
        self.log.debug('night_start: ' + str(night_start))
        time.sleep(2) # We seem to need this
        now = DateTime().getMillis()
        self.log.debug('now        : ' + str(now))

        if now >= dawn_start and now < day_start:
            curr = SOLARTIME['DAWN']
        elif now >= day_start and now < dusk_start:
            curr = SOLARTIME['DAY']
        elif now >= dusk_start and now < night_start:
            curr = SOLARTIME['DUSK']
        else:
            curr = SOLARTIME['NIGHT']

        if postUpdateCheckFirst('V_SolarTime', curr):
            self.log.info(u"Solar time is now: " + kw(SOLARTIME, curr))

addRule(AstroChannelRule())
