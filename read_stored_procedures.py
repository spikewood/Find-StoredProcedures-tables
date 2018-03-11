import re
import pprint

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
    singleLineComment = re.compile(r'.*?((\"|\').*?\2).*', re.DOTALL)
    match = singleLineComment.search(s)
    while match:
        s = s.replace(match.group(1), '>REDACTED<')
        match = singleLineComment.search(s)
    return s

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
        
    
