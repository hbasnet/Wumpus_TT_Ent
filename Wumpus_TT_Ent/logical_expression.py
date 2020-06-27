#!/usr/bin/env python

# -------------------------------------------------------------------------------
# Name:        logical_expression
# Purpose:     Contains logical_expression class, inference engine,
#              and assorted functions
#
# Created:     09/25/2011
# Last Edited: 07/22/2013
# Notes:       *This contains code ported by Christopher Conly from C++ code
#               provided by Dr. Vassilis Athitsos
#              *Several integer and string variables are put into lists. This is
#               to make them mutable so each recursive call to a function can
#               alter the same variable instead of a copy. Python won't let us
#               pass the address of the variables, so put it in a list which is
#               passed by reference. We can also now pass just one variable in
#               the class and the function will modify the class instead of a
#               copy of that variable. So, be sure to pass the entire list to a
#               function (i.e. if we have an instance of logical_expression
#               called le, we'd call foo(le.symbol,...). If foo needs to modify
#               le.symbol, it will need to index it (i.e. le.symbol[0]) so that
#               the change will persist.
#              *Written to be Python 2.4 compliant for omega.uta.edu
# -------------------------------------------------------------------------------

import sys
from copy import copy, deepcopy
# list created for symbols
symbol_collection = []
# check=[0]
# -------------------------------------------------------------------------------
# Begin code that is ported from code provided by Dr. Athitsos


class logical_expression:
    """A logical statement/sentence/expression class"""
    # All types need to be mutable, so we don't have to pass in the whole class.
    # We can just pass, for example, the symbol variable to a function, and the
    # function's changes will actually alter the class variable. Thus, lists.

    def __init__(self):
        self.symbol = ['']
        self.connective = ['']
        self.subexpressions = []


def print_expression(expression, separator):
    """Prints the given expression using the given separator"""
    if expression == 0 or expression == None or expression == '':
        print '\nINVALID\n'

    elif expression.symbol[0]:  # If it is a base case (symbol)
        sys.stdout.write('%s' % expression.symbol[0])

    else:  # Otherwise it is a subexpression
        sys.stdout.write('(%s' % expression.connective[0])
        for subexpression in expression.subexpressions:
            sys.stdout.write(' ')
            print_expression(subexpression, '')
            sys.stdout.write('%s' % separator)
        sys.stdout.write(')')


def read_expression(input_string, counter=[0]):
    """Reads the next logical expression in input_string"""
    # Note: counter is a list because it needs to be a mutable object so the
    # recursive calls can change it, since we can't pass the address in Python.
    result = logical_expression()
    length = len(input_string)
    while True:
        if counter[0] >= length:
            break

        if input_string[counter[0]] == ' ':    # Skip whitespace
            counter[0] += 1
            continue

        # It's the beginning of a connective
        elif input_string[counter[0]] == '(':
            counter[0] += 1
            read_word(input_string, counter, result.connective)
            ################################################
            # to extract all symbols and it must be unique
            element = result.symbol
            if not element[0] in symbol_collection:
                symbol_collection.append(element[0])
            #################################################
            read_subexpressions(input_string, counter, result.subexpressions)
            break

        else:  # It is a word
            read_word(input_string, counter, result.symbol)
            ################################################
            # to extract all symbols which is word and it must be unique
            element = result.symbol
            if not element[0] in symbol_collection:
                symbol_collection.append(element[0])
            #################################################
            break
    return result


def read_subexpressions(input_string, counter, subexpressions):
    """Reads a subexpression from input_string"""
    length = len(input_string)
    while True:
        if counter[0] >= length:
            print '\nUnexpected end of input.\n'
            return 0

        if input_string[counter[0]] == ' ':     # Skip whitespace
            counter[0] += 1
            continue

        if input_string[counter[0]] == ')':     # We are done
            counter[0] += 1
            return 1

        else:
            expression = read_expression(input_string, counter)
            subexpressions.append(expression)


def read_word(input_string, counter, target):
    """Reads the next word of an input string and stores it in target"""
    word = ''
    while True:
        if counter[0] >= len(input_string):
            break

        if input_string[counter[0]].isalnum() or input_string[counter[0]] == '_':
            target[0] += input_string[counter[0]]
            counter[0] += 1

        elif input_string[counter[0]] == ')' or input_string[counter[0]] == ' ':
            break

        else:
            print('Unexpected character %s.' % input_string[counter[0]])
            sys.exit(1)


def valid_expression(expression):
    """Determines if the given expression is valid according to our rules"""
    if expression.symbol[0]:
        return valid_symbol(expression.symbol[0])

    if expression.connective[0].lower() == 'if' or expression.connective[0].lower() == 'iff':
        if len(expression.subexpressions) != 2:
            print('Error: connective "%s" with %d arguments.' %
                  (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() == 'not':
        if len(expression.subexpressions) != 1:
            print('Error: connective "%s" with %d arguments.' %
                  (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() != 'and' and \
            expression.connective[0].lower() != 'or' and \
            expression.connective[0].lower() != 'xor':
        print('Error: unknown connective %s.' % expression.connective[0])
        return 0

    for subexpression in expression.subexpressions:
        if not valid_expression(subexpression):
            return 0
    return 1


def valid_symbol(symbol):
    """Returns whether the given symbol is valid according to our rules."""
    if not symbol:
        return 0

    for s in symbol:
        if not s.isalnum() and s != '_':
            return 0
    return 1

# End of ported code
# -------------------------------------------------------------------------------
# ALL FUNCTIONS code added below here


def check_true_false(entails1, entails2):
    f = open("result.txt", "w")
    if(entails1 == True and entails2 == False):
        f.write("DEFINITELY TRUE:")
        f.write("The knowledge base entails the statement, and the knowledge base does not entail the negation of the statement.")
    elif(entails1 == False and entails2 == True):
        f.write("DEFINITELY FALSE:")
        f.write("The knowledge base doesnot entails the statement, and the knowledge base entail the negation of the statement.")
    elif(entails1 == False and entails2 == False):
        f.write("Possibily true and possibily false:")
        f.write("Neither knowlwdge base entails statement nor negation of statement")
    elif(entails1 == True and entails2 == True):
        f.write("Both true and false:")
        f.write("The knowledge base entails both the statement and negation of the statement. This happens when the knowledge base is always false (i.e., when the knowledge base is false for every single row of the truth table)")
    f = open("result.txt", "r")
    print(f.read())
    f.close()


'''
def get_symbol(expression):

    symbols = []
    # print(expression.symbol[0])
    if expression.symbol[0]:
        symbols.append(expression.symbol[0])

    else:
        for sub in expression.subexpressions:
            for i in get_symbol(sub):
                if i not in symbols:
                    symbols.append(i)
    return symbols
'''


def getModel(sentence, symbols):

    dictModel = {}
    for expression in sentence.subexpressions:
        if expression.symbol[0]:
            if expression.symbol[0] in symbols:
                dictModel[expression.symbol[0]] = True
                #print "set true and removed"
                #print expression.symbol[0]
                symbols.remove(expression.symbol[0])
        elif expression.connective[0].lower() == 'not':
            if expression.subexpressions[0].symbol[0]:
                if expression.subexpressions[0].symbol[0] in symbols:
                    dictModel[expression.subexpressions[0].symbol[0]] = False
                    #print "set false and removed"
                    #print expression.subexpressions[0].symbol[0]
                    symbols.remove(expression.subexpressions[0].symbol[0])
    # print(model)
    return dictModel, symbols


def tt_entails(kb, alpha):
    symbols = deepcopy(symbol_collection)
    model, symbols = getModel(kb, symbols)

    #print(model)
    #print
    # get model of knowledge base
    '''
    model = getModel(kb)
    print(model)
    '''
    '''
    symbols = get_symbol(kb)
    symbols_alpha = get_symbol(alpha)

    for symbol in symbols_alpha:
        symbols.append(symbol)

    for symbol in model:
        if symbol in symbols:
            symbols.remove(symbol)
    '''

    return tt_check_all(kb, alpha, symbols, model)


def tt_check_all(kb, alpha, symb, model):
    print(symb)
    print(model)
    print
    #check[0] += 1
    # check if the list of symbols is empty
    if len(symb) == 0:
        # check if the sentence is true or false in the row of truth table represented by model
        # model represent truth table.....
        if PL_TRUE(kb, model):  # where KB is true and alpha is false
            return PL_TRUE(alpha, model)  # for statement
        else:
            return True
    else:
        # print check[0]
        P = symb[0]  # first
        symb.pop(0)  # rest
        return tt_check_all(kb, alpha, symb, Extended(P, True, model)) and tt_check_all(kb, alpha, symb, Extended(P, False, model))


def Extended(P, value, model):
    model[P] = value
    return model


def PL_TRUE(sentence, model):

    if sentence.symbol[0]:
        return model[sentence.symbol[0]]

    elif sentence.connective[0].lower() == 'or':
        ret = False

        for symb in sentence.subexpressions:
            ret = ret or PL_TRUE(symb, model)
        return ret

    elif sentence.connective[0].lower() == 'and':
        ret = True

        for symb in sentence.subexpressions:
            ret = ret and PL_TRUE(symb, model)
        return ret

    elif sentence.connective[0].lower() == 'xor':
        ret = False

        for symb in sentence.subexpressions:
            check_PL_TRUE = PL_TRUE(symb, model)
            ret = (ret and not check_PL_TRUE) or (
                not ret and check_PL_TRUE)
        return ret

    elif sentence.connective[0].lower() == 'iff':
        left = sentence.subexpressions[0]
        right = sentence.subexpressions[1]

        check_PL_TRUE_left = PL_TRUE(left, model)
        check_PL_TRUE_right = PL_TRUE(right, model)

        if (check_PL_TRUE_left == check_PL_TRUE_right):
            return True
        else:
            return False

    elif sentence.connective[0].lower() == 'if':
        left = sentence.subexpressions[0]
        right = sentence.subexpressions[1]

        check_PL_TRUE_left = PL_TRUE(left, model)
        check_PL_TRUE_right = PL_TRUE(right, model)

        if (check_PL_TRUE_left and not check_PL_TRUE_right):
            return False
        else:
            return True

    elif sentence.connective[0].lower() == 'not':
        check_PL_TRUE = PL_TRUE(sentence.subexpressions[0], model)
        return not check_PL_TRUE
