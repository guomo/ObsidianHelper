'''
    Module      :   utils
    Author      :   Gregory Stone — gregory@petrasoftresearch.com
    Description :   Classes to support generic vehicle abstraction.

'''
import re

#~~~~~~~~~~~~~~~~~~~~~~~~~~ UTILITY METHODS  ~~~~~~~~~~~~~~
def str_as_number(aStr, neg_ok = False):
    ''' Converts a string to the appropriate number type either float or int.
        @param (required) aStr - The number as a string to convert
        @param neg_ok - Set to true to keep negative values, otherwise default is to strip 
                        sign and return a postive num
        @raises TypeError if input wasn't a string or no numbers were in the string
    '''
    if type(aStr) is not str:
        raise TypeError("Expected str type got ${type(aStr)")

    retNum = None 
    if(neg_ok):
        cleaned = re.sub("[^\d.-]*",'',aStr)  # strip everything not sign, digits, and decimal
    else:
        cleaned = re.sub("[^\d.]*",'',aStr)  # strip everything not digits or decimal

    # Throw an exception if the string had no numbers, otherwise convert
    if len(cleaned):
        retNum = int(cleaned) if float(cleaned).is_integer() else float(cleaned)
    else:
        raise TypeError(f"No numerals found in string for conversion: {aStr}")
    return retNum


def menufy(optName, optTup):
    ''' Simple menu interfrace that enumerates a tuple and returns the chosen option #
        @param optName - Name of option to appear in the propmpt
        @param optTup - A tuple of option names to choose from

        @return tuple - Chosen # and option
    '''

    choice, good = 0, False
    print(f"Select one of the following {optName}:")
    # Display a menu of options
    for i, opt in enumerate(optTup):
        print(f"{i+1}. {opt}")
    while not good:
        try:
            choice = str_as_number(input("choice:"))
            if choice > 0 and choice < len(optTup):
                good = True
                choice = choice - 1
            else:
                print(f"That wasn't an option, pick a number between 1 and {len(optTup)+1}")
        except TypeError as ex:
            # bad input, use first choice as default
            print("That wasn't an option, try a number this time...")

    return (choice, optTup[choice])