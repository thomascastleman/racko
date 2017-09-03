
import game

class Human(game.RackoGame):

    def __init__(self):
        pass

    # returns index in rack of swap player wants to make, or None if pass
    def move(self, choice, rack):
        print "Available card: " + str(choice)
        while True:
            m = raw_input("Enter card in rack to replace or 'pass': ")

            if m.lower() == "pass":
                return None
            else:
                num = int(m)

                if num in rack:
                    return rack.index(num)
                else:
                    print "Please choose a card that's actually in the rack"