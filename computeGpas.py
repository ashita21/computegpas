# Written by Andrew Tagawa
# Version 11-29-19
import io
import string
import sys
from itertools import groupby
from operator import itemgetter

# Main function
def main(n):
    lines = [line.rstrip('\n') for line in sys.stdin]
    records = []
    for m in lines:
        ntry = m.split()
        records.append(ntry)
    output = toString(calcPadding(reduce(makeInterForm(records))))
    sys.stdout.write(output)

# Turns all letter grades into their corresponding GPA numbers
# NB: Any invalid grade that somehow gets to this point is treated as an F (0.0)
def gradeToNum(n):
    if n == "A":
        return 4.0
    elif n == "A-":
        return 3.67
    elif n == "B+":
        return 3.33
    elif n == "B":
        return 3.0
    elif n == "B-":
        return 2.67
    elif n == "C+":
        return 2.33
    elif n == "C":
        return 2.0
    elif n == "C-":
        return 1.67
    elif n == "D+":
        return 1.33
    elif n == "D":
        return 1.0
    elif n == "D-":
        return 0.67
    elif n == "F":
        return 0.0
    else:
        print("ERROR: Not a proper grade")
        return 0.0

# Removes any duplicates in a list
def removeDupes(n):
    out = []
    for m in n:
        if m not in out:
            out.append(m)
    return out

# Checks name formatting
def checkNameFormat(n1, n2):
    s1 = str(n1)
    s2 = str(n2)
    for char in s1:
        if not(char.isupper() or char.islower() or char == "-"):
            return False
    for char in s2:
        if not(char.isupper() or char.islower() or char == "-"):
            return False
    return True

# Checks for a valid grade
def checkGrade(n):
    if n == "A" or n == "A-" or n == "B+" or n == "B" or n == "B-" or n == "C+" or n == "C" or n == "C-" or n == "D+" or n == "D" or n == "D-" or n == "F":
        return True
    else:
        return False

# Checks to see if n can be an int
def tryInt(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

# Checks to see if n is an int and is not negative
def checkInt(n):
    if tryInt(n) and isinstance(int(n), int) and (int(n) >= 0):
        return True
    else:
        return False

# Removes extraneous information from records to ready them for intermediate processing
# NB: Ignores invalid inputs
def makeInterForm(n):
    out = []
    for entry in n:
        toAppend = []
        if (len(entry) == 7) and checkGrade(entry[6]) and checkNameFormat(entry[4],entry[5]) and checkInt(entry[1]) and checkInt(entry[3]):
            if (len(entry[0]) > 0 and entry[0].isupper()) and (len(entry[2]) == 1 and entry[2].isupper()):
                toAppend.append(entry[5]+", "+(entry[4])) # Name
                toAppend.append(int(entry[3])*gradeToNum(entry[6])) # Weighted Score
                toAppend.append(entry[3]) # Credit number
                toAppend.append(entry[0]) # Course dept
                toAppend.append(entry[1]) # Course number
                toAppend.append(entry[2]) # Course section
                out.append(toAppend)
    removeDupes(out)
    return out

# Compiles all student records into a single record per student and adds the header
def reduce(n):
    n.sort(key = itemgetter(0))
    i = groupby(n, itemgetter(0))
    names = [[item[0] for item in data] for (key, data) in i]
    nameList = []
    for name in names:
        nameList.append(removeDupes(name))
    out = []
    # Adding header
    out.append(["NAME","GPA","#"])

    # Calculating weighted GPA
    for name in nameList:
        e = []
        gpa = 0
        credits = 0
        for entry in n:
            if entry[0] == name[0]:
                gpa = gpa + entry[1]
                credits = credits + int(entry[2])
        e.append(name[0])
        if credits != 0:
            gpa = round(gpa/credits,2)
        else:
            gpa = "----" # Error handling for 0 total credits taken
        e.append(gpa)
        e.append(credits)
        out.append(e)

    # Checking and error handling for duplicate classes and credit differences
    for name in nameList:
        classList = []
        for entry in n:
            if entry[0] == name[0]:
                toAdd = entry[3] + " " + entry[4] + entry[5]
                classList.append(toAdd)
        seen = []
        for c in classList:
            if c not in seen:
                seen.append(c)
            else:
                print("ERROR: Multiple Enrollment (" + name[0] + ": " + c + ")")

    return out

# Pads the output
def calcPadding(n):
    maxLength = 0
    for entry in n:
        if len(entry[0]) > maxLength:
            maxLength = len(entry[0])
    for entry in n:
        padding = maxLength - len(entry[0])
        i = 0
        newStr = ""
        while i < padding+16:
            newStr = newStr + " "
            i += 1
        outStr = newStr + entry[0]
        entry[0] = outStr

    maxLength = 0
    for entry in n:
        if len(str(entry[1])) > maxLength:
            maxLength = len(str(entry[1]))
    count = 0
    for entry in n:
        padding = maxLength - len(str(entry[1]))
        i = 0
        newStr = str(entry[1])
        while i < padding:
            if count != 0:
                newStr = newStr + "0"
            else:
                newStr = newStr + " "
            i += 1
        count += 1
        entry[1] = newStr

    maxLength = 0
    for entry in n:
        if len(str(entry[2])) > maxLength:
            maxLength = len(str(entry[2]))
    for entry in n:
        padding = maxLength - len(str(entry[2]))
        i = 0
        newStr = ""
        while i < padding:
            newStr = newStr + " "
            i += 1
        outStr = newStr + str(entry[2])
        entry[2] = outStr

    return n

# Formats the output
def toString(n):
    arr = []
    i = 0
    out = ""
    for entry in n:
        toAppend = entry[0] + "  " + str(entry[1]) + "  " + str(entry[2])
        arr.append(toAppend)
    for entry in arr:
        out = out + entry + "\n"
        i += 1
    return out

#####################
#######Running#######
#####################
main(len(sys.argv))
