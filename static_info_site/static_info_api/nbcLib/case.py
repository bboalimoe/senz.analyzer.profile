__author__ = 'woodie'

import json
import sys

class Case:
    def __init__(self, case_file):
        # The json file's name
        # self.cFile      = case_file
        # The trainning case in json file
        # self.case       = self.decodeJson(case_file)
        self.case       = case_file
        # Some normal attributes of cases
        self.itemCount  = self.getItemCount()
        self.itemName   = self.getItemName()
        self.caseCount  = self.getCaseCount()
        # The list of all kinds of hypothesis
        self.hypothesis = self.getHypothesis()
        self.hypoCount  = len(self.hypothesis)
        # The list of all possible value of every item. It's a 2-demensional variable
        # - The size of itemValue is itemCount
        # - Every element of itemValue is [value0, value1, ... valuen]
        self.itemValue  = self.getItemValue()


    # Get trainning case by decoding json file
    def decodeJson(self, case_file):
        # Open the json file
        try:
            f = file(case_file)
        except IOError:
            print "File is not exist. Please check your file name."
            sys.exit()
        # decode the json data
        try:
            case = json.load(f)
        except ValueError:
            print "Json format is error. Please check your json file."
            sys.exit()
        # return the decode result
        return case

    # Get the cases in hypothesis 'h'
    def getCaseInHypo(self, h):
        case = []
        for i in range(0, self.caseCount):
            index_key = '%d' %i
            if h == self.case[index_key]["h"]:
                case.append(self.case[index_key]["case"])
        return case

    # Get the hypothesis' count in cases
    def getHypothesisCount(self, h):
        count = 0
        for i in range(0, self.caseCount):
            index_key = '%d' %i
            if h == self.case[index_key]["h"]:
                count += 1
        return count

    # Get all hypothesis from cases
    def getHypothesis(self):
        hypothesis = []
        for i in range(0, self.caseCount):
            index_key = '%d' %i
            h = self.case[index_key]["h"]
            if not h in hypothesis:
                hypothesis.append(h)
        return hypothesis

    # Get the all possible value of every item
    def getItemValue(self):
        # Init the item_value
        item_value      = {}
        # Collect all possible value of every item
        for i in range(0, self.itemCount):
            possible_values = [0]
            for j in range(0, self.caseCount):
                index_key = '%d' %j
                v = self.case[index_key]["case"][i]
                if not v in possible_values:
                    possible_values.append(v)
            item_value[i] = possible_values
        return item_value

    def getItemCount(self):
        return len(self.case["item_name"])

    def getItemName(self):
        return self.case["item_name"]

    def getCaseCount(self):
        return len(self.case)-1

    # Output the info of cases
    def printCaseInfo(self):
        print "\nTrainning Cases Infomation"
        print "=========================="
        print "- There are", self.hypoCount, "kinds of hypothesis."
        print "  They are",
        for h in self.hypothesis:
            print "[", h, "] ",
        print "\n- There are", self.caseCount, "trainning cases."
        print "- Every trainning case has", self.itemCount, "items."
        print "- Every item's possible value : "
        i = 0
        for name in self.itemName:
            print "  * ", name, ":", self.itemValue[i]
            i += 1
