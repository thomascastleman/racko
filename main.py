
import game

import debug

def main():

    r = [37, 6, 38, 1, 47, 25, 3, 5, 50, 31]
    statics = debug.determineStaticValues(r)

    print "\n\n"
    print statics


    # racko = game.RackoGame()
    # racko.start()

    # while True:
    #     racko.getMove("player2")
    #
    #     print "\n\np1 rack: ",
    #     print racko.getp1Rack()
    #
    #     print "p2 rack: ",
    #     print racko.getp2Rack()
    #
    #     print "Discard: ",
    #     print racko.getDiscard()
    #
    #     print "Mystery: ",
    #     print racko.getMys()




if __name__ == "__main__":
    main()