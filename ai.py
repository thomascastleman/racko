
import game

class AI(game.RackoGame):

    possible = []   # all possible sets of statics
    current = []    # the current set of statics being constructed via our recursive approach

    statics = []    # static values in rack

    def __init__(self):
        pass

    # get move given choice and current rack
    def move(self, choice, rack):
        return self.findPosition(choice, rack)

    # find a position in rack to exchange choice based on current rack state and static values
    def findPosition(self, choice, rack):

        # DEBUG
        print ""
        print rack
        print choice
        print self.statics

        # iterate through statics to find range in which choice fits
        i = 0
        while i < len(self.statics) and self.statics[i] < choice:
            i += 1

        # determine min and max values of range
        min = self.statics[i - 1] if i > 0 else super(AI, self).getCardMin()
        max = self.statics[i] if i < len(self.statics) else super(AI, self).getCardMax()

        # get indices in rack of min and max values, protecting edge cases
        rackIndexOfMin = rack.index(min) if i > 0 else -1
        rackIndexOfMax = rack.index(max) if i < len(self.statics) else len(rack)

        #DEBUG
        print "Min: ", min
        print "Max: ", max
        print "Min index: ", rackIndexOfMin
        print "Max index: ", rackIndexOfMax

        # if choice value in range and position available in rack (difference in indices greater than one)
        if min <= choice <= max and rackIndexOfMax - rackIndexOfMin > 1:

            # DEBUG
            print choice, " in range between ", min, ", ", max
            print "Scaling from ", min, ", ", max, " to ", rackIndexOfMin + 1, ", ", rackIndexOfMax

            # add choice to static values
            self.statics.insert(i, choice)

            # scale choice from min-max to (index min + 1)-index max
            scaled = int((float(choice - min) / float(max - min)) * float(rackIndexOfMax - (rackIndexOfMin + 1)) + (rackIndexOfMin + 1))

            # if scaled value at max index, decrement
            if scaled == rackIndexOfMax:
                scaled -= 1

            return scaled
        else:
            # pass card
            return None

    # recursively search for possible sets of initial static values
    def searchForStatics(self, rack, beg, prevStatic):
        # for every digit in subsection
        for i in range(beg, len(rack)):

            # check criteria:
            # difference between current value and previous static value needs to be > than difference in their indices
            # similarly, difference between max card value and current value needs to be >= to difference in indices
            if (rack[i] - prevStatic >= i - (beg - 1)) and super(AI, self).getCardMax() - rack[i] >= (len(rack) - 1) - i:

                # only allow difference in values to be same as difference in indices if that difference is one
                if not (rack[i] - prevStatic == i - (beg - 1) and i - (beg - 1) != 1):
                    # add to current set of statics
                    self.current.append(rack[i])
                    # search subsection from current index to end of array for more possible statics
                    self.searchForStatics(rack, i + 1, rack[i])

        # when end of rack reached, add current set to possible
        self.possible.append(list(self.current))

        if len(self.current) > 0:
            # pop current so as to go back a layer in recursion
            self.current.pop()

    # given initial rack state, determine the optimal set of values to be left unchanged throughout the game
    def determineStaticValues(self, rack):

        # get all possible set of initial static values based on rack
        self.searchForStatics(rack, 0, -1)

        # get max number of values in a set
        max = len(self.possible[0])
        for p in self.possible:
            if len(p) > max:
                max = len(p)

        optimal = []       # sets of maximum length
        ranges = []        # range of indices in rack covered each set in optimal[]

        # get all sets with max number of values, and calculate index range
        for p in self.possible:
            if len(p) == max:
                optimal.append(p)
                ranges.append(rack.index(p[len(p) - 1]) - rack.index(p[0]))

        # choose set of statics with largest range
        maxRange = ranges[0]
        for r in ranges:
            if r > maxRange:
                maxRange = r

        # update self.statics
        self.statics =  list(optimal[ranges.index(maxRange)])


    # DEBUG:
    def getStatics(self):
        return self.statics




# ________________________ PREVIOUS ________________________________

# class AI(game.RackoGame):
#
#     def __init__(self):
#         pass
#
#     def move(self, choice, rack):
#
#
#         move = self.scalingTechnique(choice, rack)
#         print "Scaling technique: " + str(move)
#         if move != None:
#             print "(where " + str(rack[move]) + " is)"
#
#
#         useProblem = False
#         p = self.getProblems(1, rack)
#         print "\nNum problems: " + str(len(p)) + " vs. rack len: " + str(len(rack))
#         if float(len(p)) / float(len(rack)) <= 0.5:
#             print "Use problem technique"
#             useProblem = True
#         else:
#             print "Probably maybe don't use problem technique"
#
#         if useProblem:
#             move = self.problemTechnique(choice, rack)
#             print "\nProblem technique: " + str(move)
#
#             if move != None:
#                 print "(where " + str(rack[move]) + " is)"
#
#         return move
#
#     # Scaling Technique:
#
#     def scalingTechnique(self, choice, rack):
#
#         index = self.getIdealPos(choice, rack)
#         choiceFit = self.getFitness(choice, index, rack)
#
#         self.current = rack[index]
#         curFit = self.getFitness(self.current, index, rack)
#
#         if choiceFit < curFit:
#             return None
#         elif choiceFit > curFit:
#             return index
#         else:
#
#             if self.getIdealPos(self.current, rack) == index:
#                 # check immediate surroundings
#
#                 if choice < self.current:
#                     if index - 1 >= 0:
#                         if self.getFitness(rack[index - 1], index - 1, rack) < self.getFitness(choice, index - 1, rack):
#                             return index - 1
#
#                     return None
#                 else:
#                     if index + 1 < len(rack):
#                         if self.getFitness(rack[index + 1], index + 1, rack) < self.getFitness(choice, index + 1, rack):
#                             return index + 1
#
#                     return None
#             else:
#                 return index
#
#     def getFitness(self, num, index, rack):
#         after = rack[index - 1] if index - 1 >= 0 else num - 1
#         before = rack[index + 1] if index + 1 < len(rack) else num + 1
#
#         # 2 if completely in order
#         if num < after and num > before:
#             return 2
#         # 1 if partially in order
#         elif num < after or num > before:
#             return 1
#         # 0 if completely out of order
#         else:
#             return 0
#
#     def getIdealPos(self, num, rack):
#         index = int(math.floor(len(rack) * (num / float(super(AI, self).getCardMax()))))
#         if index == len(rack):
#             index -= 1
#         return index
#
#     # Problem Technique:
#
#     def problemTechnique(self, choice, rack):
#         # get all locally out-of-order positions in rack
#         allProblems = []
#         for i in range(1, len(rack) / 2):
#             allProblems.append(self.getProblems(i, rack))
#
#         # intersect all problem arrays so only truly problematic positions are left
#         intersection = allProblems[0]
#         for i in range(1, len(allProblems)):
#             if len(allProblems[i]) > 0:
#                 intersection = self.intersect(intersection, allProblems[i])
#
#         # now get all positions which we could feasibly replace with our choice
#         inRange = []
#         for index in intersection:
#
#             lowerBound = rack[index - 1] + 1 if index > 0 else 1
#             upperBound = rack[index + 1] if index < len(rack) - 1 else super(AI, self).getCardMax()
#
#             if choice in range(lowerBound, upperBound):
#                 inRange.append(index)
#
#         # DEBUG
#         print "\nIn range: " + str(len(inRange))
#
#         # if no solutions
#         if len(inRange) == 0:
#             return None
#         else:
#             # otherwise choose position that is closest to ideal index of choice
#             losses = []
#             ideal = self.getIdealPos(choice, rack)
#             for index in inRange:
#                 losses.append(abs(ideal - index))
#
#             min = 0
#             for i in range(0, len(losses)):
#                 if losses[i] < losses[min]:
#                     min = i
#
#             return inRange[min]
#
#     # returns array of indices of all problems with proximity 'prox' in rack
#     def getProblems(self, prox, rack):
#         problems = []
#
#         for i in range(0, len(rack)):
#             prev = rack[i - prox] if i - prox >= 0 else rack[i] - 1
#             next = rack[i + prox] if i + prox < len(rack) else rack[i] + 1
#
#             if prev > rack[i] or next < rack[i]:
#                 problems.append(i)
#
#         return problems
#
#     # intersect two arrays a and b
#     def intersect(self, a, b):
#         intersection = []
#         for elementA in a:
#             if elementA in b:
#                 intersection.append(elementA)
#
#         return intersection