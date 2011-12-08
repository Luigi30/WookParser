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
    outputFile.write("date,time,killer,victim,weapon,headshot\n")
    for event in deathEvents:
        csvData = event.toCsv()
        outputFile.write(csvData)
    outputFile.close()
    print "Done writing CSV."