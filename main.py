import re
import BF3Events

def processEventLogFile(eventLogFile):

    deathEvents = []
    RE_XML_ILLEGAL =    u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' + \
            u'|' + \
            u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % \
            (unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
            unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
            unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
            )

    eventCounter = 0

    for line in eventLogFile:
        eventCounter += 1
        line = re.sub(RE_XML_ILLEGAL, "", line)

        if "PlayerKilled" in line:
            print "Processing event %s..." % eventCounter
            deathEvents.append(BF3Events.PlayerDeath(line))

    BF3Events.writeCsv(deathEvents)

def main():

    eventLogFile = open("20111101_events.log", mode='r')

    processEventLogFile(eventLogFile)

main()