
import game

def main():

    racko = game.RackoGame()
    racko.start()


    racko.getMove("player1")

    print "\n\np1 rack: ",
    print racko.getp1Rack()

    print "p2 rack: ",
    print racko.getp2Rack()

    print "Discard: ",
    print racko.getDiscard()

    print "Mystery: ",
    print racko.getMys()




if __name__ == "__main__":
    main()