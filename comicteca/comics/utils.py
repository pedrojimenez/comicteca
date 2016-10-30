#! /usr/local/bin/python


# ---------------------------------------------- #
def parse_int_set(inputstr="", max=1):
    """Return a set of selected values when a string formatted with ranges.

    Inout: 1-3, 6-5, 9, 12
    It will return a set with
    It accepts ascending/descending input ranges
    It checks all the numbers from all ranges are below the Max parameter
    """
    selection = set()
    invalid = set()
    # tokens are comma seperated values
    tokens = [x.strip() for x in inputstr.split(',')]
    for i in tokens:
        try:
            # typically tokens are plain old integers
            i_convert = int(i)
            if i_convert > max:
                invalid.add(i_convert)
            else:
                selection.add(i_convert)
        except:
            # if not, then it might be a range
            try:
                token = [int(k.strip()) for k in i.split('-')]
                if len(token) > 1:
                    token.sort()
                    # we have items seperated by a dash
                    # try to build a valid range
                    first = token[0]
                    last = token[len(token) - 1]
                    for x in range(first, last + 1):
                        x_convert = int(x)
                        if x_convert > max:
                            invalid.add(x_convert)
                        else:
                            selection.add(x_convert)
            except:
                # not an int and not a range...
                invalid.add(i)
    # Report invalid tokens before returning valid selection
    # print "Invalid set: " + str(invalid)
    return selection, invalid
# ---------------------------------------------- #


def main():
    print 'Generate a list of selected items!'
    inputstr = raw_input('Enter a list of items: ')

    selection = parse_int_set(inputstr)
    print 'Your selection is: '
    print str(selection)

if __name__ == "__main__":
    main()
