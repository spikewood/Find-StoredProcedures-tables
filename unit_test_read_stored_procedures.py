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
        # test that string can be normalized
        input = 'this "needs a string" --this is a comment'
        expectedResult = 'this >REDACTED< --this is a comment'
        teststring = rsp.redactString(input)
        self.assertEqual(teststring,expectedResult)

    def test_RedactStringFromMultiLine(self):
        # test that string can be normalized
        input = 'this "needs a multi-line\n string" --this is a comment'
        expectedResult = 'this >REDACTED< --this is a comment'
        teststring = rsp.redactString(input)
        self.assertEqual(teststring,expectedResult)

    def test_RedactMulitpleStringsFromMultiLine(self):
        # test that string can be normalized amongst chaos
        input = '''this "needs a multi-line
        string" 
        --this is a comment
        boom = 'this is another string' + 'another one'
        and more "commnet 'stuff' to follow"
        and 'this "one" too?'
        feel me?'''
        expectedResult = '''this >REDACTED< 
        --this is a comment
        boom = >REDACTED< + >REDACTED<
        and more >REDACTED<
        and >REDACTED<
        feel me?'''
        teststring = rsp.redactString(input)
        self.assertEqual(teststring, expectedResult)


if __name__ == '__main__':
    unittest.main()