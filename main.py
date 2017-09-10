
import game
import ai

def main():


    # DEBUG:

    rack = [45, 30, 46, 31, 47, 48, 12, 17, 50, 37]

    a = ai.AI()
    a.determineStaticValues(rack)
    print "Statics: ", a.getStatics()

    while True:
        print "\nRack: ", rack
        print "Statics: ", a.getStatics()

        choice = int(raw_input("Enter card: "))

        pos = a.findPosition(choice, rack)

        if pos == None:
            print "Card rejected"
        else:
            print "Inserting at position ", pos, " (exchange for ", rack[pos], ")"
            rack[pos] = choice


    #
    # racko = game.RackoGame()
    # racko.start()




if __name__ == "__main__":
    main()