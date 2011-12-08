import codecs
import re

def main():

# unicode invalid characters
    RE_XML_ILLEGAL =    u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' + \
                        u'|' + \
                        u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % \
                        (unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                        unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                        unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                        )

    eventLogFile = open("20111101_events.log", mode='r')

    playerKilledCount = 0
    print "Processing players killed..."

    for line in eventLogFile:
        line = re.sub(RE_XML_ILLEGAL, "", line)
        splitLine = line.split("\t")
        print splitLine
        if splitLine[3] == 'PlayerKilled':
            playerKilledCount += 1
        splitDetailText = splitLine[4].split(" ")
        #TODO: do something with that

    print 'Players killed today: %s' % playerKilledCount

main()