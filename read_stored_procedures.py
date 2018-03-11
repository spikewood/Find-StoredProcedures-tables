import re
import pprint

def cleanFile(s):
    '''Cleans a file's contents of comments and whitespace.'''
    s = cleanComments(s)
    s = removeExcessWhitespace(s)
    return s

def cleanComments(s):
    '''Removes common comments from sql files
        In the case of single line comments, the new line is not removed.'''
    s = cleanMulitLineComments(s)
    s = cleanSingleLineComments(s)
    return s

def cleanMulitLineComments(s):
    '''Multi line comments are denoted by "/* ... */"
        this function will remove these comments including newlines.'''
    singleLineComment = re.compile(r'.*?(/\*.*?\*/).*', re.DOTALL)
    match = singleLineComment.search(s)
    while match:
        s = s.replace(match.group(1), '')
        match = singleLineComment.search(s)
    return s

def cleanSingleLineComments(s):
    '''Single line comments are denoted by "--"
        this function will remove these comments without removing the entire line.'''
    singleLineComment = re.compile(r'.*?(--[^\n]*).*', re.DOTALL)
    match = singleLineComment.search(s)
    while match:
        s = s.replace(match.group(1), '')
        match = singleLineComment.search(s)
    return s

def redactString(s):
    '''redacts string denoted by starting with a " or ' and ending with the same.
        this function will change the strings to 'REDACTED'.'''
    singleLineComment = re.compile(r'.*?(((\'\'\'?)|").*?\2).*', re.DOTALL)
    match = singleLineComment.search(s)
    while match:
        s = s.replace(match.group(1), '>REDACTED<')
        match = singleLineComment.search(s)
    return s

def removeExcessWhitespace(s):
    '''removes excess whitespace front and back on the string
        also removes internal extra whitespace'''
    s = s.strip() #remove front and back whitespace
    lines = s.split('\n')
    cleanlines = []
    for line in lines: #remove excess whitespace in between words
        if line:
            words = line.split()
            line = ' '.join(words)
            cleanlines.append(line)
    cleanlines = filter(None, cleanlines)
    return '\n'.join(cleanlines)

testFile = open("CleanTestFile.sql")
input = testFile.read()
testFile.close()
teststring = cleanFile(input)


def old():

    file1 = open(
        '/Users/mwood/Downloads/Stored_Procedures_for_Reports 3/PG_CMS_REPORTS.sql')
    file1content = file1.readlines()
    file1.close()

    file2 = open(
        '/Users/mwood/Downloads/Stored_Procedures_for_Reports 3/PG_REPORTS.sql')
    file2content = file2.readlines()
    file2.close()

    procedureRegex = re.compile(r'^(procedure) +(\w+)', re.IGNORECASE)
    tableColumnRegex = re.compile(r' ([a-z]\w+)\.([a-z]\w+) ', re.IGNORECASE)

    procedures = []
    tables = {}
    newfile = []

    for linenum in range(len(file1content)):
        match = procedureRegex.search(file1content[linenum])
        if match:
            procedures.append(match.group(2))
            newfile.append(match.group(0))
        else:
            match = tableColumnRegex.search(file1content[linenum])
            if match:
                keyRegex = re.compile(r' (\w+) '+match.group(1)+'[ ,]')
                table = match.group(1)
                for i in range(linenum+1,0,-1):
                    backmatch = keyRegex.search(file1content[i])
                    if backmatch:
                        table = backmatch.group(1)
                        print('found '+str(i)+': '+backmatch.group(1))
                        break
                    elif procedureRegex.search(file1content[i]):
                        table = match.group(1)
                        print('not found '+str(i)+':'+match.group(1))
                        break

                tables.setdefault(table,[])
                tables[table].append(match.group(2))
                newfile.append(match.group(0))

    for key in tables:
        tables[key] = set(tables[key])
        tables[key] = list(tables[key])
        
    
