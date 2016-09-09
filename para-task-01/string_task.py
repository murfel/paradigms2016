# Given a string, if its length is at least 3,
# add 'ing' to its end.
# Unless it already ends in 'ing', in which case
# add 'ly' instead.
# If the string length is less than 3, leave it unchanged.
# Return the resulting string.
#
# Example input: 'read'
# Example output: 'reading'
def verbing(s):
    if len(s) >= 3:
        if s[-3:] == 'ing':
            s = s + 'ly'
        else:
            s = s + 'ing'
    return s


# Given a string, find the first appearance of the
# substring 'not' and 'bad'. If the 'bad' follows
# the 'not', replace the whole 'not'...'bad' substring
# with 'good'.
# Return the resulting string.
#
# Example input: 'This dinner is not that bad!'
# Example output: 'This dinner is good!'
def not_bad(s):

    # Alternatively:
    #not_ind = s.find('not')
    #bad_ind = s.find('bad')
    #...

    # More alternatively:
    #import re
    ## The regex should be like '([\S\s]*)not[\s\S]*bad([\s\S]*)'
    ## (see regexr.com/3e6go) Any suggestions?
    #m = re.search('', s)
    #if m:
    #    s = m.group(0) + 'good' + m.group(1)
    #return s

    found_not = False
    found_bad = False
    for i in range(len(s) - 2):
        if not found_not:
            if s[i:i + 3] == 'not':
                found_not = True
                not_ind = i
        if not found_bad:
            if s[i:i + 3] == 'bad':
                found_bad = True
                bad_ind = i

    if found_not and found_bad and (not_ind < bad_ind):
        s = s[:not_ind] + 'good' + s[bad_ind + 3:]

    return s


# Consider dividing a string into two halves.
# If the length is even, the front and back halves are the same length.
# If the length is odd, we'll say that the extra char goes in the front half.
# e.g. 'abcde', the front half is 'abc', the back half 'de'.
#
# Given 2 strings, a and b, return a string of the form
#  a-front + b-front + a-back + b-back
#
# Example input: 'abcd', 'xy'
# Example output: 'abxcdy'
def front_back(a, b):
    from math import ceil
    a_mid = ceil(len(a) / 2)
    b_mid = ceil(len(b) / 2)

    return a[:a_mid] + b[:b_mid] + a[a_mid:] + b[b_mid:]
