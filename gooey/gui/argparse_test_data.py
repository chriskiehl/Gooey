'''
Created on Jan 16, 2014

@author: Chris
'''
from argparse import ArgumentParser

parser = ArgumentParser(description='Example Argparse Program')
parser.add_argument("filename", help="Name of the file you want to read")  # positional
parser.add_argument("outfile", help="Name of the file where you'll save the output")  # positional
parser.add_argument('-T', '--tester', choices=['yes', 'no'], help="Yo, what's up man? I'm a help message!")  # Choice
parser.add_argument('-m', '--moutfile',
                    help='Redirects output to the file specified by you, the awesome user')  # Optional
parser.add_argument('-v', '--verbose', help='Toggles verbosity off')  # Optional
parser.add_argument('-s', '--schimzammy', help='Add in an optional shimzammy parameter')  # Optional
parser.add_argument('-e', '--repeat', action='count', help='Set the number of times to repeat')  # Counter
parser.add_argument('-c', '--constoption', action="store_const", const="myconstant",
                    help='Make sure the const action is correctly sorted')  # Flag
parser.add_argument('-t', '--truify', action="store_true", help='Ensure the store_true actions are sorted')  # Flag
parser.add_argument('-f', '--falsificle', action="store_false",
                    help='Ensure the store_false actions are sorted')  # Flag


