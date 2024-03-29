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
    def toCsv(self):
        #Standard toCsv function for events with only an eventDate/Time/playerName.
        return "NULL,\"%s\",\"%s\",\"%s\"\n" % (self.eventDate, self.eventTime, self.playerName)

class PlayerJoinEvent(BF3BaseEvent):
    #eventDate: date of event
    #eventTime: time of event
    #playerName: player name
    
    def __init__(self, type, eventData):
        self.type = type
        self.tableName = 'playerjoin'

        splitLine = eventData.split("\t")
        splitTime = splitLine[1].split(" ")

        #get the time
        self.eventDate = logDateToSqlDate(splitTime[0])
        self.eventTime = splitTime[1]
        self.playerName = splitLine[4].split(" ")[0].rstrip("\n")

class PlayerLeaveEvent(BF3BaseEvent):
    #eventDate: date of event
    #eventTime: time of event
    #playerName: player name

    def __init__(self, type, eventData):
        self.type = type
        self.tableName = 'playerleave'

        splitLine = eventData.split("\t")
        splitTime = splitLine[1].split(" ")

        #get the time
        self.eventDate = logDateToSqlDate(splitTime[0])
        self.eventTime = splitTime[1]
        self.playerName = splitLine[4].split(" ")[0].rstrip("\n")

class PlayerSuicideEvent(BF3BaseEvent):
    #eventDate: date of event
    #eventTime: time of event
    #playerName: player name

    def __init__(self, type, eventData):
        self.type = type
        self.tableName = 'playersuicide'

        splitLine = eventData.split("\t")
        splitTime = splitLine[1].split(" ")

        #get the time
        self.eventDate = logDateToSqlDate(splitTime[0])
        self.eventTime = splitTime[1]
        self.playerName = splitLine[4].split(" ")[0].rstrip("\n")

class PlayerSwitchedTeamsEvent(BF3BaseEvent):
    #eventDate: date of event
    #eventTime: time of event
    #playerName: player name
    #oldTeam: old team
    #newTeam: new team

    def __init__(self, type, eventData):
        self.type = type
        self.tableName = 'playerswitchedteams'

        splitLine = eventData.split("\t")
        splitTime = splitLine[1].split(" ")

        #get the time
        self.eventDate = logDateToSqlDate(splitTime[0])
        self.eventTime = splitTime[1]

        extData = splitLine[4].split(" ")

        self.playerName = extData[0]

        if extData[4] == "Neutral":
            self.oldTeam = "Neutral"
            self.newTeam = extData[6] + " " + extData[7]
        else:
            self.oldTeam = extData[4] + " " + extData[5]
            self.newTeam = extData[7] + " " + extData[8]

    def toCsv(self):
        return "NULL,\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"" %\
               (self.eventDate, self.eventTime, self.playerName, self.oldTeam, self.newTeam)

class PlayerSwitchedSquadsEvent(BF3BaseEvent):
    #eventDate: date of event
    #eventTime: time of event
    #playerName: player name
    #oldSquad: old team
    #newSquad: new team

    def __init__(self, type, eventData):
        self.type = type
        self.tableName = 'playerswitchedsquads'

        splitLine = eventData.split("\t")
        splitTime = splitLine[1].split(" ")

        #get the time
        self.eventDate = logDateToSqlDate(splitTime[0])
        self.eventTime = splitTime[1]

        extData = splitLine[4].split(" ")

        self.playerName = extData[0]

        self.oldSquad = extData[4]
        self.newSquad = extData[6]

    def toCsv(self):
        return "NULL,\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"" %\
               (self.eventDate, self.eventTime, self.playerName, self.oldSquad, self.newSquad)

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
        self.tableName = 'playerkilled'

        splitLine = deathLine.split("\t")
        splitTime = splitLine[1].split(" ")

        self.eventDate = logDateToSqlDate(splitTime[0])
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

        #special cases because DICE is inconsistent :dice:
        if 'Roadkill' in splitLine[4]:
            self.weapon = "Roadkill"
        elif 'Assault' in splitLine[4]:
            self.weapon = "F2000 Assault"
        elif 'LMG' in splitLine[4]:
            self.weapon = "M60 LMG"
        elif 'SAW' in splitLine[4]:
            self.weapon = "M249 SAW"
        elif 'Snayperskaya' in splitLine[4]:
            self.weapon = "SV98 Snayperskaya"
        elif 'Combat' in splitLine[4]:
            self.weapon = "870 Combat"
        elif 'M1911' in splitLine[4]:
            self.weapon = "WWII M1911 .45"
        elif 'Pistol' in splitLine[4]:
            self.weapon = "M9 Pistol"
        else:
            self.weapon = splitKill[4].rstrip("}]\n")

    def toCsv(self):
        #format: date,time,killer,victim,weapon,headshot
        return "NULL,\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"\n" \
            % (self.eventDate, self.eventTime, self.playerName, self.victim, self.weapon, self.headshot)

def writeCsv(eventList):
    type = eventList[0].type #fetch the type of event list we've been sent and use that as the CSV name
    outputFile = open((type + ".csv"), "a")
    for event in eventList:
        csvData = event.toCsv()
        outputFile.write(csvData)
    outputFile.close()

def sqlInsertEvents(db, eventList):
    type = eventList[0].type #fetch the type of event list we've been sent and use that as the CSV name
    outputFile = open((type + ".csv"), "a")
    if eventList[0].tableName != 'playerkilled':
        for event in eventList:
            db.query("INSERT INTO %s VALUES(NULL, '%s', '%s', '%s')" % (event.tableName, event.eventDate, event.eventTime, db.escape_string(event.playerName)))
    else:
        for event in eventList:
            db.query("INSERT INTO playerkilled VALUES(NULL, '%s', '%s', '%s', '%s', '%s', '%s')" % (event.eventDate, event.eventTime, db.escape_string(event.playerName), db.escape_string(event.victimName), db.escape_string(event.weapon), event.headshot))
    outputFile.close()

def logDateToSqlDate(date):
	sqlDate = (date[6:10] + "-" + date[0:2] + "-" + date[3:5])
	return sqlDate