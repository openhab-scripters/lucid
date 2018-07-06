import os
import lucid.config as lucidconfig

def autoremote(message, ttl=300, sender='openHAB'):
    '''
    Sends an autoremote message
    '''

    # Use GCM Server for delivery
    cmd = 'curl -s -G "https://autoremotejoaomgcd.appspot.com/sendmessage" ' \
        + '--data-urlencode "key='+lucidconfig.autoremote['key']+'" ' \
        + '--data-urlencode "password='+lucidconfig.autoremote['password']+'" ' \
        + '--data-urlencode "message='+message+'" ' \
        + '--data-urlencode "sender='+sender+'" ' \
        + '--data-urlencode "ttl='+str(ttl)+'" ' \
        + ' > /dev/null'

    os.system(cmd)
