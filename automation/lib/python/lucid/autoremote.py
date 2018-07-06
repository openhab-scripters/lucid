import os

def autoremote(message, ttl=300, sender='openHAB'):
    '''
    Sends an autoremote message
    '''

    ARPassw = 'secret'
    ARKey = 'LONG-KEY-GOES-HERE'

    # Use GCM Server for delivery
    cmd = 'curl -s -G "https://autoremotejoaomgcd.appspot.com/sendmessage" ' \
        + '--data-urlencode "key='+ARKey+'" ' \
        + '--data-urlencode "password='+ARPassw+'" ' \
        + '--data-urlencode "message='+message+'" ' \
        + '--data-urlencode "sender='+sender+'" ' \
        + '--data-urlencode "ttl='+str(ttl)+'" ' \
        + ' > /dev/null'

    os.system(cmd)
