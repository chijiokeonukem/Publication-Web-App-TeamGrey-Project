from os import path
import unittest

from comp62521.database import database
from comp62521 import views

class TestDatabase(unittest.TestCase):


def test_sorting(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))

        #Test cases fo publications summary
        data = db.get_publication_summary()

        #Test case1: Test sorting of column Details
        self.assertNotEquals(data,views.sorting(data, 1)) #case: sorted
        self.assertEquals(data,views.sorting(data, 1)) #case: unSorted

        #Test case2: Test sorting of column conf_papers
        self.assertNotEquals(data,views.sorting(data, 2))
        self.assertEquals(data,views.sorting(data, 2))

        #Test case3: Test sorting of column journal
        self.assertNotEquals(data,views.sorting(data, 3))
        self.assertEquals(data,views.sorting(data, 3))

        #Test case4: Test sorting of column book
        self.assertNotEquals(data,views.sorting(data, 4))
        self.assertEquals(data,views.sorting(data, 4))

        #Test case5: Test sorting of column book_chapter
        self.assertNotEquals(data,views.sorting(data, 5))
        self.assertEquals(data,views.sorting(data, 5))
