__author__ = 'woodie'

import case
import decimal

# @class:       Naive Bayes Classifier
# @author:      Woodie
# @createAt:    Wed 10 Dec, 2014
# @description:
# Bayes Formula:
#       - P(male|D) = P(male) * P(D|male) / P(D)
#       - P(female|D) = P(female) * P(D|female) / P(D)
#   The Result Probability:
#       - P'(male|D) = P(male|D) / ( P(male|D) + P(female|D) )
#       - P'(female|D) = P(female|D) / ( P(male|D) + P(female|D) )

class NBC:
    def __init__(self, train_file):
        # Get trainning cases from json file.
        self.tCase = case.Case(train_file)
        self.tCase.printCaseInfo()
        # The list of hypothesis
        # It's a list.
        self.hypothesis = self.tCase.hypothesis
        # It's the size of equivalent sample, it's used to avoid underestimate
        self.equivalentSample = []
        # It's the item's prior probability at different hypothesis, it's used to avoid underestimate
        self.priorProbabiltyOfItem = []
        # Init the size of equivalent sample and the item's prior probability at different hypothesis
        for i in range(0, self.tCase.itemCount):
            self.equivalentSample.append(0)
            for j in self.tCase.itemValue[i]:
                count = len(self.tCase.itemValue[i])
                p     = 1 / decimal.Decimal(count) # It's one probability of items, default is the average
                prior = [] # It's the every probability of items
                for x in range(0, count):
                    prior.append(p)
                self.priorProbabiltyOfItem.append(prior)
        # The prior probability of every hypothesis
        # It is a list.
        self.prior_p = {}
        # Every item's likelihood at certain hypothesis. It's a 3-dimensional list variable
        # - 1. The size of likelihood is case's item count
        # - 2. Every element of likelihood is [H0, H1, ... Hi ... Hn]
        #   Hi contains the item's every possible result's possibility in Hi (that is likelihood's definition)
        # - 3. Hi's structure is [li0, li1, ... lij ... lim]
        #   lij is the likelihood of items in Hi which result is j
        self.likelihood = []
        self.trainningOverFlag = False

    # The prediction of new case
    # It's a normalization method
    def predictCase(self, D):
        # Check the trainning is over
        if self.trainningOverFlag == False:
            print "Please train NBC first!"
            return "unknown"
        #start classifying ...
        print "\nThe classifying started"
        print "======================="

        # Init tmp variable
        result = {}
        P = 0

        # Check unclassified case
        if not self.checkUnclassifiedCase(D):
            return "unknown"

        # Calculate the Denominator
        for h in self.hypothesis:
            P += self.posteriorP(h, D)
            print "- the posterior true probability of", h, "is", self.posteriorP(h, D)

        # Calculate the Molecular
        try:
            for h in self.hypothesis:
                p = self.posteriorP(h, D) / P
                result[h] = p
            return result
        except:
            print "The result is not accuracy enough. Please add more trainning cases."
            return "unknown"
            #return result

    # It will train the NBC by calculating various of probability with cases' data
    # First, it calcutates the prior probability of every hypothesis.
    def train(self, m="notInput", p="notInput"):
        # Avoid the underestimate
        if not self.checkUnderestimateParam(m, p):
            return
        # Init tmp variable
        itemCount = self.tCase.itemCount
        itemValue = self.tCase.itemValue

        # Init likelihood
        for i in range(0, itemCount):
            hi = {}
            for h in self.hypothesis:
                vi = []
                for v in range(0, len(itemValue[i])):
                    l = 0
                    vi.append(l)
                hi[h] = vi
            self.likelihood.append(hi)

        #start trainning ...
        print "\nThe trainning started"
        print "====================="
        print "\n1. Calculate the prior probability of every hypothesis"
        print "------------------------------------------------------"

        # Calculate the prior probability of every hypothesis
        for hypo in self.hypothesis:
            p = self.priorP(hypo)
            print "The", hypo, "in cases weighs", p, "%"
            #self.prior_p.append(p)
            self.prior_p[hypo] = p

        print "\n2. Calculate every item's likelihood at certain hypothesis"
        print "----------------------------------------------------------"

        # Calculate every item's likelihood at certain hypothesis
        for i in range(0, itemCount):
            print i, ".",
            for h in self.hypothesis:
                for v in range(0, len(itemValue[i])):
                    # likelihood[i][h][v] = P(i=v|h)
                    self.likelihood[i][h][v] = self.likelihoodP(i, h, v)
                    print self.likelihood[i][h][v],
                    if v < len(itemValue[i]) - 1:
                        print "|",
                print " , ",
            print "\n"
        self.trainningOverFlag = True

    # The posterior probability of hypothesis - P(h|D)( * P(D) )
    # - h is hypothesis' name
    # - D is the new case which is waitting for classifying (D = [])
    def posteriorP(self, h, D):
        P = 0
        # Calculate the prior probability
        P = self.prior_p[h]
        for i in range(0, len(D)):
            # Calculate the posterior probability
            P = P * self.likelihood[i][h][D[i]]
            #print self.hypothesis[index_h]
        return P

    # The prior probability of hypothesis - P(h)
    def priorP(self, h):
        h_count = self.tCase.getHypothesisCount(h)
        total_count = self.tCase.caseCount
        P = float(h_count) / float(total_count)
        return P

    # The likelihood of D at a certain hypothesis - P(D|h)
    # - P(itemIndex = value | h)
    # - h is the hypothesis' name
    # - itemIndex, value are index number
    def likelihoodP(self, itemIndex, h, value):
        # avoid underestimate
        # P(D|h) = P(item = value | h) =  count(item = value & hypothesis = h) / count(hypothesis = h)
        #        = (nc + m * p)/(n + m)  =  (count(item = value & hypothesis = h) + m * p)/(count(hypothesis = h) + m)
        m = self.equivalentSample[itemIndex]
        p = self.priorProbabiltyOfItem[itemIndex][value]
        # The cases in hypothesis 'h'
        caseInHypo = self.tCase.getCaseInHypo(h)
        # The count of cases in hypothesis 'h'
        countCaseInHypo = len(caseInHypo)
        # The count of cases in hypothesis 'h' which item 'itemIndex' is 'value'
        countCaseItemIsValue = 0
        for case in caseInHypo:
            if case[itemIndex] == value:
                countCaseItemIsValue += 1
        # The likelihood
        P = (float(countCaseItemIsValue + m * p)) / (float(countCaseInHypo + m))
        return P

    # Check the unclassified case's rule
    def checkUnclassifiedCase(self, D):
        # Check the D's len
        if len(D) != self.tCase.itemCount:
            print "The count of unclassified case's item is error. Please check your unclassified case."
            return False
        # Check the size of every item in D
        index = 0
        for i in D:
            if not i in self.tCase.itemValue[index]:
                print "The value of item", index, "(D[", index, "]=", i, ") is illegal. Please select the value which is exist in case.json"
                return False
            index += 1
        return True

    def checkUnderestimateParam(self, m, p):
        print "\nCheck the underestimate params"
        print "=============================="
        if m != "notInput" and p != "notInput":
            # Check the len of m
            if len(m) != self.tCase.itemCount:
                print "Error! Tranning is stopped."
                print "The length of equivalent sample is error."
                return False
            # Check the len of p
            if len(p) != self.tCase.itemCount:
                print "Error! Tranning is stopped."
                print "The length of probability of items is error."
                return False

            for i in range(0, self.tCase.itemCount):
                # Check size of equivalentSample
                if m[i] < 0 :
                    print "Error! Tranning is stopped."
                    print "The", i, "th item's equivalent sample size is illegal."
                    return False
                # Check every probability of items is in (0,1)
                total_p = 0
                for j in p[i]:
                    if j >= 1 or j <= 0:
                        print "Error! Tranning is stopped."
                        print "The", i+1, "th item's", j+1, "th probability is illegal."
                        return False
                    total_p += j
                # Check total of each probability of items is 1
                if total_p != 1:
                    print "Error! Tranning is stopped."
                    print "The total of", i+1, "th probability is not 1."
                    return False
            # Check over
            self.equivalentSample = m
            self.priorProbabiltyOfItem = p
            print "Set the size of equivalent sample and the prior probability of items successfully."
            return True
        elif m == "notInput" and p == "notInput":
            print "Ignore the underestimate."
            return True
        else:
            print "Error! Tranning is stopped."
            print "If you want to avoid the underestimate, please fill all param."
            return False

    def generateTrainResult(self):
        data = {
            "hypothesis":  self.hypothesis,
            "priorP":      self.prior_p,
            "likelihoodP": self.likelihood
        }
        return data




