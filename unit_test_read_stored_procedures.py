import unittest
import read_stored_procedures as rsp

class TestCleanCommentMethods(unittest.TestCase):

    def test_cleanSingleLineCommentFromSingleLine(self):
        # test that a single comment can be removed from the string
        input = '--this is a comment'
        expectedResult = ''
        teststring = rsp.cleanComments(input)
        self.assertEqual(teststring,expectedResult)

    def test_cleanSingleLineCommentFromMulipleLines(self):
        # test that a single comment can be removed from mulitple lined string
        input = 'hi there\n--this is a comment\nand this is the end'
        expectedResult = 'hi there\n\nand this is the end'
        teststring = rsp.cleanComments(input)
        self.assertEqual(teststring, expectedResult)

    def test_cleanMultipleSingleLineCommentsFromMultipleLines(self):
        # test that a single comment can be removed from the string
        input = '''-- hi
        hi there
        --this is a comment
        --and this is a comment
        and this is the middle
        -- and this is another comment
        and this is the end
        -- bye bye'''
        expectedResult = '''
        hi there
        
        
        and this is the middle
        
        and this is the end
        '''
        teststring = rsp.cleanComments(input)
        self.assertEqual(teststring, expectedResult)

    def test_cleanMultipleLineCommentsFromMultipleLines(self):
        # test that a single comment can be removed from the string
        input = '''hi
        /*hi there
        this is a comment
        and this is a comment
        */and this is the middle
        and this is the end'''
        expectedResult = '''hi
        and this is the middle
        and this is the end'''
        teststring = rsp.cleanComments(input)
        self.assertEqual(teststring, expectedResult)

    def test_cleanMultipleTypesOfCommentsFromMultipleLines(self):
        # test that a single comment can be removed from the string
        input = '''hi
        /*hi there
        --this is a comment
        and this is a comment
        */and this is the middle
        -- this is a comment
        and this is the end'''
        expectedResult = '''hi
        and this is the middle
        
        and this is the end'''
        teststring = rsp.cleanComments(input)
        self.assertEqual(teststring, expectedResult)

class TestRedactStringMethods(unittest.TestCase):

    def test_RedactStringFromSingleLine(self):
        # test that string can be normalized in single line strings
        input = 'this "needs a string" --this is a comment'
        expectedResult = 'this >REDACTED< --this is a comment'
        teststring = rsp.redactString(input)
        self.assertEqual(teststring,expectedResult)

    def test_RedactStringFromMultiLine(self):
        # test that strings can be normalized in multiline strings
        input = 'this \'\'needs a multi-line\n string\'\' --this is a comment'
        expectedResult = 'this >REDACTED< --this is a comment'
        teststring = rsp.redactString(input)
        self.assertEqual(teststring,expectedResult)

    def test_RedactMulitpleStringsFromMultiLine(self):
        # test that strings can be normalized amongst chaos
        input = '''this "needs a multi-line
        string" 
        --this is a comment
        boom = ''this is another string'' + \'\'\'another one\'\'\'
        and more \'\'\'commnet 'stuff' to follow\'\'\'
        and ''this 'one' too?''
        feel me?'''
        expectedResult = '''this >REDACTED< 
        --this is a comment
        boom = >REDACTED< + >REDACTED<
        and more >REDACTED<
        and >REDACTED<
        feel me?'''
        teststring = rsp.redactString(input)
        self.assertEqual(teststring, expectedResult)

class TestRemoveExcessWhitespaceMethods(unittest.TestCase):

    def test_trimWhitespaceFrontAndBack(self):
        # test that strings can be normalized
        input = '   this "needs a string" --this is a comment   '
        expectedResult = 'this "needs a string" --this is a comment'
        teststring = rsp.removeExcessWhitespace(input)
        self.assertEqual(teststring,expectedResult)

    def test_trimWhitespaceInside(self):
        # test that strings can be normalized
        input = '   this  "needs a string" \t  \r\n--this is a comment   '
        expectedResult = 'this "needs a string"\n--this is a comment'
        teststring = rsp.removeExcessWhitespace(input)
        self.assertEqual(teststring,expectedResult)

    def test_trimMultipleNewLines(self):
        # test that strings can be normalized
        input = '\n   this  "needs\n\n\n\n a string" \t  \r\n\n--this is a comment   \n'
        expectedResult = 'this "needs\na string"\n--this is a comment'
        teststring = rsp.removeExcessWhitespace(input)
        self.assertEqual(teststring,expectedResult)

class TestCleanTestFile(unittest.TestCase):

    def test_cleanTestFile(self):
        # test that strings can be normalized
        testFile = open("CleanTestFile.sql")
        input = testFile.read()
        testFile.close()
        resultFile = open("CleanResultFile.sql")
        expectedResult = resultFile.read()
        resultFile.close()
        teststring = rsp.cleanFile(input)
        self.assertEqual(teststring,expectedResult)

if __name__ == '__main__':
    unittest.main()