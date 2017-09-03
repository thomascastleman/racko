
import game
import math

class AI(game.RackoGame):

    def __init__(self):
        pass

    def move(self, choice, rack):

        # Still debugging

        move = self.scalingTechnique(choice, rack)
        print "Scaling technique: " + str(move)
        if move != None:
            print "(where " + str(rack[move]) + " is)"


        useProblem = False
        p = self.getProblems(1, rack)
        print "\nNum problems: " + str(len(p)) + " vs. rack len: " + str(len(rack))
        if float(len(p)) / float(len(rack)) <= 0.5:
            print "Use problem technique"
            useProblem = True
        else:
            print "Probably maybe don't use problem technique"

        if useProblem:
            move = self.problemTechnique(choice, rack)
            print "\nProblem technique: " + str(move)

            if move != None:
                print "(where " + str(rack[move]) + " is)"

        return move

    # Scaling Technique:

    def scalingTechnique(self, choice, rack):

        index = self.getIdealPos(choice, rack)
        choiceFit = self.getFitness(choice, index, rack)

        current = rack[index]
        curFit = self.getFitness(current, index, rack)

        if choiceFit < curFit:
            return None
        elif choiceFit > curFit:
            return index
        else:

            if self.getIdealPos(current, rack) == index:
                # check immediate surroundings

                if choice < current:
                    if index - 1 >= 0:
                        if self.getFitness(rack[index - 1], index - 1, rack) < self.getFitness(choice, index - 1, rack):
                            return index - 1

                    return None
                else:
                    if index + 1 < len(rack):
                        if self.getFitness(rack[index + 1], index + 1, rack) < self.getFitness(choice, index + 1, rack):
                            return index + 1

                    return None
            else:
                return index

    def getFitness(self, num, index, rack):
        after = rack[index - 1] if index - 1 >= 0 else num - 1
        before = rack[index + 1] if index + 1 < len(rack) else num + 1

        # 2 if completely in order
        if num < after and num > before:
            return 2
        # 1 if partially in order
        elif num < after or num > before:
            return 1
        # 0 if completely out of order
        else:
            return 0

    def getIdealPos(self, num, rack):
        index = int(math.floor(len(rack) * (num / float(super(AI, self).getCardMax()))))
        if index == len(rack):
            index -= 1
        return index

    # Problem Technique:

    def problemTechnique(self, choice, rack):
        # get all locally out-of-order positions in rack
        allProblems = []
        for i in range(1, len(rack) / 2):
            allProblems.append(self.getProblems(i, rack))

        # intersect all problem arrays so only truly problematic positions are left
        intersection = allProblems[0]
        for i in range(1, len(allProblems)):
            if len(allProblems[i]) > 0:
                intersection = self.intersect(intersection, allProblems[i])

        # now get all positions which we could feasibly replace with our choice
        inRange = []
        for index in intersection:

            lowerBound = rack[index - 1] + 1 if index > 0 else 1
            upperBound = rack[index + 1] if index < len(rack) - 1 else super(AI, self).getCardMax()

            if choice in range(lowerBound, upperBound):
                inRange.append(index)

        # DEBUG
        print "\nIn range: " + str(len(inRange))

        # if no solutions
        if len(inRange) == 0:
            return None
        else:
            # otherwise choose position that is closest to ideal index of choice
            losses = []
            ideal = self.getIdealPos(choice, rack)
            for index in inRange:
                losses.append(abs(ideal - index))

            min = 0
            for i in range(0, len(losses)):
                if losses[i] < losses[min]:
                    min = i

            return inRange[min]

    # returns array of indices of all problems with proximity 'prox' in rack
    def getProblems(self, prox, rack):
        problems = []

        for i in range(0, len(rack)):
            prev = rack[i - prox] if i - prox >= 0 else rack[i] - 1
            next = rack[i + prox] if i + prox < len(rack) else rack[i] + 1

            if prev > rack[i] or next < rack[i]:
                problems.append(i)

        return problems

    # intersect two arrays a and b
    def intersect(self, a, b):
        intersection = []
        for elementA in a:
            if elementA in b:
                intersection.append(elementA)

        return intersection