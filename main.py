import re
import BF3Events
import urllib2

def processEventLogFile(eventLogFile):
    #Import a log file object and do whatever processing we're doing.

    #Fetch the goon list.
    response = urllib2.urlopen('http://reg.davejk.net/Tools/List')
    html = response.read()
    goonList = html.split("\r\n")

    deathEvents = []
    joinEvents = []
    leaveEvents = []
    suicideEvents = []
    teamSwitchEvents = []
    squadSwitchEvents = []
    eventCounter = 0

    print "Erasing old .CSV files if they exist..."

    playerJoinCsv = open("playerJoin.csv", "w")
    playerLeaveCsv = open("playerLeave.csv", "w")
    playerSuicideCsv = open("playerSuicide.csv", "w")
    playerSwitchedTeamsCsv = open("playerSwitchedTeams.csv", "w")
    playerSwitchedSquadsCsv = open("playerSwitchedSquads.csv", "w")
    playerKilledCsv = open("playerKilled.csv", "w")

    playerJoinCsv.close()
    playerLeaveCsv.close()
    playerSuicideCsv.close()
    playerSwitchedSquadsCsv.close()
    playerSwitchedTeamsCsv.close()
    playerKilledCsv.close()

    for line in eventLogFile:
        eventCounter += 1 #keep a running total of events
        line = removeNulls(line) #remove the u0000 characters

        if "PlayerJoin" in line:
            for name in goonList[0:(goonList.__len__() - 1)]:
                if name in line:
                    print "Event %s: PlayerJoin" % eventCounter
                    joinEvents.append(BF3Events.PlayerJoinEvent("PlayerJoin", line))
                    break
            else:
                print "Event %s: PlayerJoin (Not involving goons, not written.)" % eventCounter

        if "PlayerLeave" in line:
            for name in goonList[0:(goonList.__len__() - 1)]:
                if name in line:
                    print "Event %s: PlayerLeave" % eventCounter
                    leaveEvents.append(BF3Events.PlayerLeaveEvent("PlayerLeave", line))
                    break
            else:
                print "Event %s: PlayerLeave (Not involving goons, not written.)" % eventCounter

        if "PlayerSuicide" in line:
            for name in goonList[0:(goonList.__len__() - 1)]:
                if name in line:
                    print "Event %s: PlayerSuicide" % eventCounter
                    suicideEvents.append(BF3Events.PlayerSuicideEvent("PlayerSuicide", line))
                    break
            else:
                print "Event %s: PlayerSuicide (Not involving goons, not written.)" % eventCounter

        if "PlayerSwitchedTeams" in line:
            for name in goonList[0:(goonList.__len__() - 1)]:
                if name in line:
                    print "Event %s: PlayerSwitchedTeams" % eventCounter
                    teamSwitchEvents.append(BF3Events.PlayerSwitchedTeamsEvent("PlayerSwitchedTeams", line))
                    break
            else:
                print "Event %s: PlayerSwitchedTeams (Not involving goons, not written.)" % eventCounter

        if "PlayerSwitchedSquads" in line:
            for name in goonList[0:(goonList.__len__() - 1)]:
                if name in line:
                    print "Event %s: PlayerSwitchedSquads" % eventCounter
                    squadSwitchEvents.append(BF3Events.PlayerSwitchedSquadsEvent("PlayerSwitchedSquads", line))
                    break
            else:
                print "Event %s: PlayerSwitchedSquads (Not involving goons, not written.)" % eventCounter

        if "PlayerKilled" in line:
            i = -1
            for name in goonList[0:(goonList.__len__() - 1)]:
                i += 1
                if name in line:
                    print "Event %s: PlayerKilled (%s, entry %s)" % (eventCounter, name, i)
                    deathEvents.append(BF3Events.PlayerKilledEvent("PlayerKilled", line))
                    break
            else:
                print "Event %s: PlayerKilled (Not involving goons, not written.)" % eventCounter

    print "Processing PlayerJoin events..."
#    for event in joinEvents:
    BF3Events.writeCsv(joinEvents)

    print "Processing PlayerLeave events..."
#    for event in leaveEvents:
    BF3Events.writeCsv(leaveEvents)

    print "Processing PlayerSuicide events..."
#    for event in suicideEvents:
    BF3Events.writeCsv(suicideEvents)

    print "Processing PlayerKilled events..."
 #   for event in deathEvents:
    BF3Events.writeCsv(deathEvents)

    print "Processing PlayerSwitchedTeams events..."
#    for event in teamSwitchEvents:
    BF3Events.writeCsv(teamSwitchEvents)

    print "Processing PlayerSwitchedSquads events..."
#    for event in squadSwitchEvents:
    BF3Events.writeCsv(squadSwitchEvents)

    print "Done processing."

def removeNulls(line):
    #procon is really dumb and spits out a u0000 null after every character!?
    #run this function on log files we're working on so python can understand them

    RE_XML_ILLEGAL =    u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' + \
        u'|' + \
        u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % \
        (unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
        unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
        unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
        )

    line = re.sub(RE_XML_ILLEGAL, "", line)
    return line

def main():

    eventLogFile = open("20111101_events.log", mode='r')

    processEventLogFile(eventLogFile)

main()