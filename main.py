import codecs
import re

class PlayerDeath:

    #A PlayerDeath event consists of the following data:
    #eventDate: date of event
    #eventTime: time of event
    #killer: killer name
    #victim: victim name
    #weapon: the murder weapon
    #headshot: was it a headshot true/false?

    def __init__(self, deathLine):
    # unicode invalid characters

        splitLine = deathLine.split("\t")
        splitTime = splitLine[1].split(" ")

        #get the time
        self.eventDate = splitTime[0]
        self.eventTime = splitTime[1]

        #is it a headshot?
        if 'headshot' in splitLine[4]:
            self.headshot = True
        else:
            self.headshot = False

        #now get killer/victim/weapon out of splitLine[4]
        #splitLine[4] looks like:
        #   Capped1 killed IncredulousDylan [{MISSING: global.Weapons.svd} | -HEADSHOT-]\n
        #or
        #   Scinon killed Sosnitoonsa [Roadkill]
        
        splitKill = splitLine[4].split(" ")
        self.killer = splitKill[0]
        self.victim = splitKill[2]

        if 'Roadkill' in splitLine[4]: 
            self.weapon = "Roadkill"
        else:
            self.weapon = splitKill[4].rstrip("}]\n")

    def toCsv(self):
        #format: date,time,killer,victim,weapon,headshot
        return "%s,%s,%s,%s,%s,%s\n" % (self.eventDate, self.eventTime, self.killer,
                                        self.victim, self.weapon, self.headshot)
        
def writeCsv(deathEvents):
    outputFile = open("output.csv", "w")
    for event in deathEvents:
        csvData = event.toCsv()
        outputFile.write(csvData)
    outputFile.close()
    print "Done writing CSV."

def main():

    deathEvents = []

    RE_XML_ILLEGAL =    u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' + \
            u'|' + \
            u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % \
            (unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
            unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
            unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
            )

    eventLogFile = open("20111101_events.log", mode='r')

    eventCounter = 0

    for line in eventLogFile:
        eventCounter += 1
        line = re.sub(RE_XML_ILLEGAL, "", line)

        if "PlayerKilled" in line:
            print "Processing event %d..." % eventCounter
            deathEvents.append(PlayerDeath(line))

    writeCsv(deathEvents)

main()