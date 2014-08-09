'''
Created on Jan 25, 2014

@author: Chris
'''

import unittest
import i18n_config

# from i18n import I18N

#
class Test(unittest.TestCase):
  #   def setUp(self):
  #     pass
  #
  # def testI18nThrowsIOErrorOnBadPath(self):
  #   with self.assertRaises(IOError):
  #     I18N('franch')

  def test_asfasdfadsf(self):
    import i18n
    print i18n.CONFIG_LANG
    i18n.CONFIG_LANG = "aaaa"
    print i18n.CONFIG_LANG
    reload(i18n)
    print i18n.CONFIG_LANG

if __name__ == "__main__":
  pass
  #import sys;sys.argv = ['', 'Test.testName']
  unittest.main()
