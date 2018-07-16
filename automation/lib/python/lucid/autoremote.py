import os
import lucid.config as config

def autoremote(message, ttl=300, sender='openHAB'):
    '''
    Sends an autoremote message
    '''

    # Use GCM Server for delivery
    cmd = 'curl -s -G "https://autoremotejoaomgcd.appspot.com/sendmessage" ' \
        + '--data-urlencode "key='+config.autoremote['key']+'" ' \
        + '--data-urlencode "password='+config.autoremote['password']+'" ' \
        + '--data-urlencode "message='+message+'" ' \
        + '--data-urlencode "sender='+sender+'" ' \
        + '--data-urlencode "ttl='+str(ttl)+'" ' \
        + ' 1>/dev/null 2>&1 &'

    os.system(cmd)
