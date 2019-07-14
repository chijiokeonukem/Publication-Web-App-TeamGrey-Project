from os import path
import unittest

from comp62521.database import database
from comp62521 import views

class TestDatabase(unittest.TestCase):

def test_calculate_first_last(self):
self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-2.xml")))
self.assertEqual(db.calculate_first_last_sole(), (('Author', 'First Author', 'Last Author', 'Sole Author'),
                                                  [[u'AUTHOR1', 2, 0, 1], [u'AUTHOR3', 0, 0, 0],
                                                   [u'AUTHOR4', 0, 2, 0], [u'AUTHOR2', 0, 0, 1]]))

#testcase3 database = sprint-2-acceptance-3.xml
self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-3.xml")))
self.assertEqual(db.calculate_first_last_sole(), (('Author', 'First Author', 'Last Author', 'Sole Author'),
                                                  [[u'AUTHOR', 0, 0, 9], [u'AUTHOR1', 0, 0, 1]]))
