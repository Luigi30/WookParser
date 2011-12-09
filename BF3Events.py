########################################################################
#   BF3Events
#
#   There should be a class in here for every possible event in the log:
#       PlayerKilled
#       PlayerJoin
#       PlayerLeave
#       PlayerSuicide
#       PlayerSwitchedTeams
#       PlayerSwitchedSquads
########################################################################

class BF3BaseEvent:
    def writeCsv(self, eventList):
        #one type entry for each type of event.
        outputFile = open((self.type + ".csv"), "a")
        csvData = self.toCsv()
        outputFile.write(csvData)
        outputFile.close()

    def toCsv(self):
        #Standard toCsv function for events with only an eventDate/Time/playerName.
        return "%s,%s,%s\n" % (self.eventDate, self.eventTime, self.playerName)

class PlayerJoinEvent(BF3BaseEvent):
    #eventDate: date of event
    #eventTime: time of event
    #playerName: player name
    
    def __init__(self, type, eventData):
        self.type = type

        splitLine = eventData.split("\t")
        splitTime = splitLine[1].split(" ")

        #get the time
        self.eventDate = splitTime[0]
        self.eventTime = splitTime[1]
        self.playerName = splitLine[3]

class PlayerLeaveEvent(BF3BaseEvent):
    #eventDate: date of event
    #eventTime: time of event
    #playerName: player name

    def __init__(self, type, eventData):
        self.type = type

        splitLine = eventData.split("\t")
        splitTime = splitLine[1].split(" ")

        #get the time
        self.eventDate = splitTime[0]
        self.eventTime = splitTime[1]
        self.playerName = splitLine[3]

class PlayerSuicideEvent(BF3BaseEvent):
    #eventDate: date of event
    #eventTime: time of event
    #playerName: player name

    def __init__(self, type, eventData):
        self.type = type

        splitLine = eventData.split("\t")
        splitTime = splitLine[1].split(" ")

        #get the time
        self.eventDate = splitTime[0]
        self.eventTime = splitTime[1]
        self.playerName = splitLine[3]

class PlayerKilledEvent(BF3BaseEvent):

    #A PlayerKilled event consists of the following data:
    #eventDate: date of event
    #eventTime: time of event
    #playerName: killer name
    #victim: victim name
    #weapon: the murder weapon
    #headshot: was it a headshot true/false?

    #Input is a de-nulled event line from the log file.

    def __init__(self, type, deathLine):

        #set the type
        self.type = type

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
        self.playerName = splitKill[0]
        self.victim = splitKill[2]

        if 'Roadkill' in splitLine[4]:
            self.weapon = "Roadkill"
        else:
            self.weapon = splitKill[4].rstrip("}]\n")

    def toCsv(self):
        #format: date,time,killer,victim,weapon,headshot
        return "%s,%s,%s,%s,%s,%s\n" % (self.eventDate, self.eventTime, self.playerName,
                                        self.victim, self.weapon, self.headshot)