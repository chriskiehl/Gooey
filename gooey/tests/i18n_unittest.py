# '''
# Created on Jan 25, 2014
#
# @author: Chris
# '''
#
# import unittest
#
# import i18n
#
#
# class Test(unittest.TestCase):
#
#   def test_i18n_loads_module_by_name(self):
#     self.assertTrue(i18n._DICTIONARY is None)
#
#     i18n.load('english')
#     self.assertTrue(i18n._DICTIONARY is not None)
#     self.assertEqual('Cancel', i18n._('cancel'))
#
#     i18n.load('french')
#     self.assertEqual('Annuler', i18n._('cancel'))
#
#
#   def test_i18n_throws_exception_on_no_lang_file_found(self):
#     self.assertRaises(IOError, i18n.load, 'chionenglish')
#
#
#
#
#
# if __name__ == "__main__":
#   pass
#   #import sys;sys.argv = ['', 'Test.testName']
#   unittest.main()
