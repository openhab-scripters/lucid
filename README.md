# lucid <!-- omit in toc --> 

**lucid** is an openHAB jsr223 Jython helper library. It's a derivative work based on [Steve Bate](https://github.com/steve-bate)'s great project [openHab2-jython](https://github.com/OH-Jython-Scripters/openhab2-jython).

**lucid** takes openHAB Jython scripting to a higher level and can be used for general scripting purposes, including defining rules, triggers and conditions. **lucid** aims to be easy to use and to provide a good documentation. (The documentation work has just begun)

## Content <!-- omit in toc --> 

- [Getting Started with lucid](#getting-started-with-lucid)
    - [Prerequisites](#prerequisites)
    - [Installing](#installing)
    - [Set up logging](#set-up-logging)
    - [Test your lucid installation](#test-your-lucid-installation)
    - [Configuration file](#configuration-file)
    - [Example scripts](#example-scripts)
- [Writing scripts](#writing-scripts)
- [Contributing](#contributing)
    - [Native english speakers](#native-english-speakers)
    - [openHAB Jython Scripting on Slack](#openhab-jython-scripting-on-slack)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Disclaimer](#disclaimer)

## Getting Started with lucid

These instructions will get you **lucid** up and running on your openHAB server.

### Prerequisites

- [openHAB](https://docs.openhab.org/index.html) version **2.3** or later
- The [Experimental Next-Gen Rule Engine](https://www.openhab.org/docs/configuration/rules-ng.html) add-on must be installed in openHAB 2.

### Installing

* Follow the documentation to install [JSR223 Jython Scripting](https://www.openhab.org/docs/configuration/jsr223-jython.html) unless you already done that. Now, according to the documentation you have already set the `EXTRA_JAVA_OPTS` environment variable in `/etc/default/openhab2` to something similar to this example:

   ```
  EXTRA_JAVA_OPTS=-Xbootclasspath/a:/home/pi/jython2.7.0/jython.jar \
  -Dpython.home=/home/pi/jython2.7.0 \
  -Dpython.path=/etc/openhab2/automation/lib/python
   ```
   The last line in the example above defines the path where openHAB can find your jython library files. You can choose a different directory for your installation. We prefer using the directory `/etc/openhab2/automation/lib/python` (The [JSR223 Jython Scripting](https://www.openhab.org/docs/configuration/jsr223-jython.html) documentation uses a different lib directory which is also OK) We will now simply refer to that directory as the **LIB-DIR**. It's the directory where openHAB will look for your jython library files.

* Download the [lucid archive file](https://github.com/OH-Jython-Scripters/lucid/archive/master.zip), extract it in a temporary location and transfer the [lucid](https://github.com/OH-Jython-Scripters/lucid/tree/master/automation/lib/python/lucid) folder together with all its content (found in the zip file's automation/lib/python folder) into your LIB-DIR. 
* Change the owner, group and file permissions. E.g. cd into the LIB-DIR. and run `sudo chown -R openhab:openhab lucid` followed by `sudo chmod -R 664 lucid`

### Set up logging
You'd probably want to configure logging for lucid in the config file for logging. The config file for logging is org.ops4j.pax.logging.cfg located in the userdata/etc folder (manual setup) or in /var/lib/openhab2/etc (apt/deb-based setup). See the [documentation](https://www.openhab.org/docs/administration/logging.html#config-file). In the `OSGi appender` section, after line `log4j2.logger.org_eclipse_smarthome_automation.name = org.eclipse.smarthome.automation`, add
   ```
   log4j2.logger.lucid.level = DEBUG
   log4j2.logger.lucid.name = lucid
   ```

### Test your lucid installation
Put the [helloWorld.py](https://raw.githubusercontent.com/OH-Jython-Scripters/lucid/master/Script%20Examples/helloWorld.py) file from the examples in your `automation/jsr223` directory and watch the openHAB log file carefully. It should output "Hello world from lucid!" once every minute. Delete the `helloWorld.py` file when you are done.

### Configuration file
For some functionality, like the ability to send autoremote messages for example, there is some configuration to do. In LIB-DIR/lucid, rename the file example_config.py to config.py and edit the file to suit your needs. It should be quite self explanatory what it's all about. The configuration file can be used to store config entries for all your jython scripts. You can use it like this:
```python
import lucid.config as config
if (config.somerandomdata['anumber'] == 0):
    # Do something
```

Some script packages based on **lucid** may assume that you have defined a configuration file so it's recommended that you create one now.

### Example scripts
You are now ready to make your own scripts using lucid. Have a look at the [examples](https://github.com/OH-Jython-Scripters/lucid/tree/master/Script%20Examples) or continue at [Writing scripts](#writing-scripts).

## Writing scripts
In order for your jython scripts to work with lucid, they need to
* Import mandatory libraries
* Define one or more rule classes with functions that return what triggers you wish to use and an execute function which is where you define what should be executed when the triggers fire.
* Add the rule class to the automation manager.

For example:
```python
from lucid.rules import rule, addRule
from lucid.triggers import ItemStateChangeTrigger
from logging import DEBUG, INFO, WARNING, ERROR

@rule
class ExampleRule(object):
    def getEventTriggers(self):
        return [
            ItemStateChangeTrigger('My_TestSwitch_1'),
        ]

    def execute(self, modules, inputs):
        self.log.info('Something has happened')

addRule(ExampleRule())
```

## Contributing
There are several ways to contribute to this project.

### Native english speakers
We'd need some help from native english speakers to correct and improve this documentation regarding the language.

### openHAB Jython Scripting on Slack
OH-Jython-Scripters now has a Slack channel! It will help us to make sense of our work, and drive our efforts in Jython scripting forward. So if you are just curious, got questions, need support or just like to hang around, don't hesitate, join [**openHAB Jython Scripting on Slack**](https://join.slack.com/t/besynnerlig/shared_invite/enQtMzI3NzIyNTAzMjM1LTdmOGRhOTAwMmIwZWQ0MTNiZTU0MTY0MDk3OTVkYmYxYjE4NDE4MjcxMjg1YzAzNTJmZDM3NzJkYWU2ZDkwZmY) <--- Click link!

## License

This project is licensed under the [Eclipse Public License 1.0](https://opensource.org/licenses/EPL-1.0)

## Acknowledgments

* [Steve Bate](https://github.com/steve-bate) made [openHab2-jython](https://github.com/OH-Jython-Scripters/openhab2-jython), the great work from which **lucid** is derived from.

## Disclaimer
THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
