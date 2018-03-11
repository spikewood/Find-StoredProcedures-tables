import unittest
import read_stored_procedures as rsp

class TestCleanMethods(unittest.TestCase):

    def test_cleanSingleLineCommentFromSingleLine(self):
        # test that a single comment can be removed from the string
        singleLineCommentString = '--this is a comment'
        expectedResult = ''
        teststring = rsp.cleanComments(singleLineCommentString)
        self.assertEqual(teststring,expectedResult)

    def test_cleanSingleLineCommentFromMulipleLines(self):
        # test that a single comment can be removed from mulitple lined string
        singleLineCommentString = 'hi there\n--this is a comment\nand this is the end'
        expectedResult = 'hi there\n\nand this is the end'
        teststring = rsp.cleanComments(singleLineCommentString)
        self.assertEqual(teststring, expectedResult)

    def test_cleanMultipleSingleLineCommentsFromMultipleLines(self):
        # test that a single comment can be removed from the string
        singleLineCommentString = '''-- hi
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
        teststring = rsp.cleanComments(singleLineCommentString)
        self.assertEqual(teststring, expectedResult)

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
