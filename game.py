
import random

class RackoGame(object):

    player1 = None
    player2 = None

    p1Rack = []
    p2Rack = []

    mysteryStack = []   # stack of unused cards
    discardStack = []   # stack of discarded cards

    cardMin = 1         # minimum card value
    cardMax = 50        # maximum card value
    rackLength = 10     # capacity of rack


    def __init__(self):

        import ai, human
        self.player1 = ai.AI()
        self.player2 = human.Human()

        # randomize mystery stack
        nums = []
        for n in range(self.cardMin, self.cardMax + 1):
            nums.append(n)

        while len(nums) > 0:
            n = nums[random.randrange(0, len(nums))]
            self.mysteryStack.append(n)
            nums.remove(n)

        # deal cards to each rack
        for i in range(0, 10):
            self.p1Rack.append(self.mysteryStack.pop())
            self.p2Rack.append(self.mysteryStack.pop())


    def start(self):

        # flip over first card in mystery stack to start
        self.discardStack.append(self.mysteryStack.pop())



        # DEBUG
        print self.discardStack
        print self.mysteryStack

        print "p1:"
        print self.p1Rack
        print "p2:"
        print self.p2Rack

        print "\n\n\n"




        # while neither player has won
        # while not self.checkWin(self.p1Rack) and not self.checkWin(self.p2Rack):
        #     self.getMove("player2")
        #     self.getMove("player1")


    def getMove(self, player_):

        player = self.player1 if player_ == "player1" else self.player2
        rack = self.p1Rack if player_ == "player1" else self.p2Rack

        # get choice
        choice = self.discardStack.pop()

        # DEBUG:
        print "Choice is " + str(choice)

        move = player.move(choice, rack)

        if move == None:

            # DEBUG:
            print "DISCARDING CHOICE"

            # discard choice
            self.discardStack.append(choice)

            # get mystery
            mystery = self.mysteryStack.pop()

            # DEBUG
            print "Mystery is " + str(mystery)


            move = player.move(mystery, rack)

            if move == None:

                #DEBUG
                print "DISCARDING MYSTERY"

                # discard
                self.discardStack.append(mystery)
            else:
                # exchange
                rack = self.exchange(mystery, move, rack)
        else:
            # exchange
            rack = self.exchange(choice, move, rack)

        if player_ == "player1":
            self.p1Rack = rack
        else:
            self.p2Rack = rack



    def exchange(self, card, index, rack):
        self.discardStack.append(rack[index])       # discard swapped card from rack
        rack[index] = card                          # replace card with choice
        return rack

    def checkWin(self, rack):
        if sorted(rack) == rack:
            return True
        else:
            return False



    def getCardMax(self):
        return self.cardMax

    # DEBUG:

    def getp1Rack(self):
        return self.p1Rack
    def getp2Rack(self):
        return self.p2Rack
    def getDiscard(self):
        return self.discardStack
    def getMys(self):
        return self.mysteryStack