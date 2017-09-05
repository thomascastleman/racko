
import random

class RackoGame(object):

    # players
    player1 = None
    player2 = None

    # player racks
    p1Rack = []
    p2Rack = []

    mysteryStack = []   # stack of unused cards
    discardStack = []   # stack of discarded cards

    cardMin = 1         # minimum card value
    cardMax = 50        # maximum card value
    rackLength = 10     # capacity of rack


    def __init__(self):

        # initialize players
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
        for i in range(0, self.rackLength):
            self.p1Rack.append(self.mysteryStack.pop())
            self.p2Rack.append(self.mysteryStack.pop())

        # allow AI to perform initial setup
        self.player1.determineStaticValues(self.p1Rack)

    # initiate rack-o game
    def start(self):

        # flip over first card in mystery stack to start
        self.discardStack.append(self.mysteryStack.pop())

        print self.p1Rack
        print self.player1.getStatics()

        # while neither player has won
        while not self.checkWin(self.p1Rack) and not self.checkWin(self.p2Rack):
            self.getMove("player2")
            self.getMove("player1")

            print ""
            print "AI Rack: ", self.p1Rack
            print "Human Rack: ", self.p2Rack
            print ""

    # given player, get move
    def getMove(self, player_):

        # select player and rack
        player = self.player1 if player_ == "player1" else self.player2
        rack = self.p1Rack if player_ == "player1" else self.p2Rack

        choice = self.discardStack.pop()    # get choice card
        move = player.move(choice, rack)    # get player move based on choice

        # if player chooses to discard
        if move == None:
            self.discardStack.append(choice)    # discard choice

            mystery = self.mysteryStack.pop()   # get mystery card
            move = player.move(mystery, rack)   # get player move based on mystery

            # if choosing to discard mystery
            if move == None:
                # discard
                self.discardStack.append(mystery)
            else:
                # exchange
                rack = self.exchange(mystery, move, rack)
        else:
            # exchange
            rack = self.exchange(choice, move, rack)

        # update actual rack
        if player_ == "player1":
            self.p1Rack = rack
        else:
            self.p2Rack = rack

    # exchange a card for another at a given index in rack
    def exchange(self, card, index, rack):
        self.discardStack.append(rack[index])       # discard card already in rack
        rack[index] = card                          # replace card with choice
        return rack

    # check if rack is in win-state (sorted)
    def checkWin(self, rack):
        if sorted(rack) == rack:
            return True
        else:
            return False

    # getters and setters:

    def getCardMax(self):
        return self.cardMax

    def getCardMin(self):
        return self.cardMin