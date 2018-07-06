# lucid
A lucid openHAB jsr223 Jython helper library

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## About
lucid is a library providing helper functions for easy and lucid jsr223 jython scripting in openHab version 2.3 and later.

## openHAB Jython Scripting on Slack
OH-Jython-Scripters now has a Slack channel! It will help us to make sense of our work, and drive our efforts in Jython scripting forward. So if you are just curious, got questions, need support or just like to hang around, do not hesitate, join [**openHAB Jython Scripting on Slack**](https://join.slack.com/t/besynnerlig/shared_invite/enQtMzI3NzIyNTAzMjM1LTdmOGRhOTAwMmIwZWQ0MTNiZTU0MTY0MDk3OTVkYmYxYjE4NDE4MjcxMjg1YzAzNTJmZDM3NzJkYWU2ZDkwZmY) <--- Click link!

## Installation
* Follow the documentation to install [JSR223 Jython Scripting](https://www.openhab.org/docs/configuration/jsr223-jython.html) unless you already done that. Now, according to the documentation you have already set the EXTRA_JAVA_OPTS environment variable in /etc/default/openhab2 to something similar to this example:
```
EXTRA_JAVA_OPTS=-Xbootclasspath/a:/home/pi/jython2.7.0/jython.jar \
  -Dpython.home=/home/pi/jython2.7.0 \
  -Dpython.path=/etc/openhab2/lib/python
```
The last line in the example above defines the path where openHAB can find your jython library files. You might have choosen a different directory for your installation. We will now simply refer to that directory as the **LIB-DIR**. It's the directory where openHAB will look for your jython library files.

* Download the [lucid zip file](https://github.com/OH-Jython-Scripters/lucid/archive/master.zip), extract it in a temporary location and transfer the complete lucid folder to your LIB-DIR.
* Change the owner, group and file permissions. E.g. cd into the LIB-DIR. and run `chown -R openhab:openhab lucid` followed by `chmod -R 664 lucid`

* Put the demo.py file in your `automation/jsr223` directory and watch the openHAB log file carefully.

* You are now ready to make your own scripts based on lucid. Have a look at the examples.

#### Prerequisits
* [openHAB](https://docs.openhab.org/index.html) version **2.3** or later

## Disclaimer
THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
