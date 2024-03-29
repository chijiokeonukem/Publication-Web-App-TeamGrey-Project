from os import path
import unittest

from comp62521.database import database
from comp62521 import views

class TestDatabase(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")

    def test_read(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        self.assertEqual(len(db.publications), 1)

    def test_read_invalid_xml(self):
        db = database.Database()
        self.assertFalse(db.read(path.join(self.data_dir, "invalid_xml_file.xml")))

    def test_read_missing_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "missing_year.xml")))
        self.assertEqual(len(db.publications), 0)

    def test_read_missing_title(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "missing_title.xml")))
        # publications with missing titles should be added
        self.assertEqual(len(db.publications), 1)

    def test_get_average_authors_per_publication(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-1.xml")))
        _, data = db.get_average_authors_per_publication(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.3, places=1)
        _, data = db.get_average_authors_per_publication(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 2, places=1)
        _, data = db.get_average_authors_per_publication(database.Stat.MODE)
        self.assertEqual(data[0], [2])

    def test_get_average_publications_per_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-2.xml")))
        _, data = db.get_average_publications_per_author(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 1.5, places=1)
        _, data = db.get_average_publications_per_author(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 1.5, places=1)
        _, data = db.get_average_publications_per_author(database.Stat.MODE)
        self.assertEqual(data[0], [0, 1, 2, 3])

    def test_get_average_publications_in_a_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-3.xml")))
        _, data = db.get_average_publications_in_a_year(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.5, places=1)
        _, data = db.get_average_publications_in_a_year(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 3, places=1)
        _, data = db.get_average_publications_in_a_year(database.Stat.MODE)
        self.assertEqual(data[0], [3])

    def test_get_average_authors_in_a_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-4.xml")))
        _, data = db.get_average_authors_in_a_year(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.8, places=1)
        _, data = db.get_average_authors_in_a_year(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 3, places=1)
        _, data = db.get_average_authors_in_a_year(database.Stat.MODE)
        self.assertEqual(data[0], [0, 2, 4, 5])
        # additional test for union of authors
        self.assertEqual(data[-1], [0, 2, 4, 5])

    def test_get_publication_summary(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publication_summary()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data[0]), 6,
            "incorrect number of columns in data")
        self.assertEqual(len(data), 2,
            "incorrect number of rows in data")
        self.assertEqual(data[0][1], 1,
            "incorrect number of publications for conference papers")
        self.assertEqual(data[1][1], 2,
            "incorrect number of authors for conference papers")

    def test_get_average_authors_per_publication_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "three-authors-and-three-publications.xml")))
        header, data = db.get_average_authors_per_publication_by_author(database.Stat.MEAN)
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 3,
            "incorrect average of number of conference papers")
        self.assertEqual(data[0][1], 1.5,
            "incorrect mean journals for author1")
        self.assertEqual(data[1][1], 2,
            "incorrect mean journals for author2")
        self.assertEqual(data[2][1], 1,
            "incorrect mean journals for author3")

    def test_get_publications_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publications_by_author()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 2,
            "incorrect number of authors")
        self.assertEqual(data[0][-1], 1,
            "incorrect total")

    def test_get_average_publications_per_author_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_average_publications_per_author_by_year(database.Stat.MEAN)
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")

    def test_get_publications_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publications_by_year()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")

    def test_get_author_totals_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_author_totals_by_year()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")
        self.assertEqual(data[0][1], 2,
            "incorrect number of authors in result")
    
    def test_degrees_of_separation(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir,"sprint4_task1.xml")))
        self.assertEquals(db.degrees_of_separation("C","D"),1)
        self.assertEquals(db.degrees_of_separation("A","B"),0)
        self.assertEquals(db.degrees_of_separation("E","C"),2)
        self.assertEquals(db.degrees_of_separation("A","F"),'X')

    def test_calculate_first_last(self):
        db = database.Database()
        #testcase1 database = sprint-2-acceptance-1.xml
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-1.xml")))
        self.assertEqual(db.calculate_first_last_sole(), (('Author', 'First Author', 'Last Author', 'Sole Author'),
                                                          [[u'AUTHOR1', 1, 1, 0], [u'AUTHOR2', 0, 1, 0],
                                                           [u'AUTHOR3', 0, 1, 0], [u'AUTHOR4', 2, 0, 0]]))

        #testcase2 database = sprint-2-acceptance-2.xml
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-2.xml")))
        self.assertEqual(db.calculate_first_last_sole(), (('Author', 'First Author', 'Last Author', 'Sole Author'),
                                                          [[u'AUTHOR1', 2, 0, 1], [u'AUTHOR3', 0, 0, 0],
                                                           [u'AUTHOR4', 0, 2, 0], [u'AUTHOR2', 0, 0, 1]]))

        #testcase3 database = sprint-2-acceptance-3.xml
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-3.xml")))
        self.assertEqual(db.calculate_first_last_sole(), (('Author', 'First Author', 'Last Author', 'Sole Author'),
                                                          [[u'AUTHOR', 0, 0, 9], [u'AUTHOR1', 0, 0, 1]]))

    def test_StatsForAuthor(self):
            db = database.Database()
            self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
            #test1
            self.assertEqual(db.StatsForAuthor("Stefano Ceri"), (218, 100, 94, 18, 6, 230, 78, 28, 43, 4, 3, 25, 10, 10, 5, 0, 8, 7, 0, 1, 0))
            #test2
            self.assertEqual(db.StatsForAuthor("Piero Fraternali"), (49, 29, 18, 1, 1, 49, 0, 0, 0, 0, 0, 7, 3, 3, 0, 1, 0, 0, 0, 0, 0))
            #test3
            self.assertEqual(db.StatsForAuthor("ABC"), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

    '''def test_sorting(self):
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
        self.assertEquals(data,views.sorting(data, 5))'''

    def test_calculate_authors_details(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint3_task1_acc1.xml")))
        self.assertEqual(db.calculate_authors_details(),(('Author', 'First Author', 'Last Author', 'Sole Author'),
                                                         ('Journals', 'Conference Papers','Books', 'Book Chapters'),
                                                         [['AUTHOR1',1,1,0,0,0,0,0,0,0,0,0,0],
                                                         ['AUTHOR2',1,1,1,0,0,0,0,0,0,0,0,0]]))
        self.assertTrue(db.read(path.join(self.data_dir, "sprint3_task1_acc2.xml")))
        self.assertEqual(db.calculate_authors_details(),(('Author', 'First Author', 'Last Author', 'Sole Author'),
                                                         ('Journals', 'Conference Papers','Books', 'Book Chapters'),
                                                         [['AUTHOR1',1,1,1,0,0,0,0,0,0,0,0,0],
                                                         ['AUTHOR2',1,1,1,0,0,0,0,0,0,0,0,0]]))
        self.assertTrue(db.read(path.join(self.data_dir, "sprint3_task1_acc3.xml")))
        self.assertEqual(db.calculate_authors_details(),(('Author', 'First Author', 'Last Author', 'Sole Author'),
                                                         ('Journals', 'Conference Papers','Books', 'Book Chapters'),
                                                         [['AUTHOR1',0,0,0,1,1,1,0,0,0,0,0,0],
                                                         ['AUTHOR2',0,0,0,1,1,1,0,0,0,0,0,0]]))
        self.assertTrue(db.read(path.join(self.data_dir, "sprint3_task1_acc4.xml")))
        self.assertEqual(db.calculate_authors_details(),(('Author', 'First Author', 'Last Author', 'Sole Author'),
                                                         ('Journals', 'Conference Papers','Books', 'Book Chapters'),
                                                         [['AUTHOR1',0,0,0,0,0,0,1,1,1,0,0,0],
                                                         ['AUTHOR2',0,0,0,0,0,0,1,1,1,0,0,0]]))
        self.assertTrue(db.read(path.join(self.data_dir, "sprint3_task1_acc5.xml")))
        self.assertEqual(db.calculate_authors_details(),(('Author', 'First Author', 'Last Author', 'Sole Author'),
                                                         ('Journals', 'Conference Papers','Books', 'Book Chapters'),
                                                         [['AUTHOR1',0,0,0,0,0,0,0,0,0,1,1,1],
                                                         ['AUTHOR2',0,0,0,0,0,0,0,0,0,1,1,1]]))
        self.assertTrue(db.read(path.join(self.data_dir, "sprint3_task1_acc6.xml")))
        self.assertEqual(db.calculate_authors_details(),(('Author', 'First Author', 'Last Author', 'Sole Author'),
                                                         ('Journals', 'Conference Papers','Books', 'Book Chapters'),
                                                         [['AUTHOR1',1,1,1,1,1,1,1,1,1,1,1,1],
                                                         ['AUTHOR2',1,1,1,1,1,1,1,1,1,1,1,1]]))

    def test_searchAuthor(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        self.assertEqual(db.calculate_searchAuthors("testName"),(0,0,0,0,0,0,0,0))

        #Test case1: Number of publications
        #self.assertEqual(db.calculate_searchAuthors("Carlo Batini"),(10,0,0,0,0,0))

        #Test case2: Number of conference papers
        #self.assertEqual(db.calculate_searchAuthors("Carlo Batini"),(10,6,0,0,0,0))

        #Test case3: Number of journals
        #self.assertEqual(db.calculate_searchAuthors("Carlo Batini"),(10,6,3,0,0,0))

        #Test case4: Number of book chapters
        #self.assertEqual(db.calculate_searchAuthors("Carlo Batini"),(10,6,3,0,0,0))

        #Test case5: Number of books
        #self.assertEqual(db.calculate_searchAuthors("Carlo Batini"),(10,6,3,0,1,0,0,0))

        #Test case6: Number of co-Authors
        #self.assertEqual(db.calculate_searchAuthors("Carlo Batini"),(10,6,3,0,1,15,0,0))

        #Test case7: Number of first
        #self.assertEqual(db.calculate_searchAuthors("Carlo Batini"),(10,6,3,0,1,15,3,0))

        #Test case8: Number of last
        self.assertEqual(db.calculate_searchAuthors("Carlo Batini"),(10,6,3,0,1,15,3,5))

        #Test case8: Test final
        self.assertEqual(db.calculate_searchAuthors("Stefano Ceri"),(218,100,94,18,6,230,78,25))

	#Testing for author search by entering part of the authors name (Sprint3 Task 4)
    def test_search_part_name(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))

        #Test case1: Test for search_part_name
        #self.assertEqual(db.calculate_searchPartName("sam"),['Pedro R. Falcone Sampaio', 'Sandra de F. Mendes Sampaio', 'Fredrik Samson', 'Pierangela Samarati', 'Samuel Madden', 'Sam Guinea', 'Sandra Sampaio'])
        self.assertTrue(db.read(path.join(self.data_dir, "sprint3_task3.xml")))
        #self.assertEquals(db.calculate_searchPartName("sam"),['Alice Sam','Brian Sam','Alice Sammer','Brian Sammer','Alice Samming','Brian Samming',
        #                                                      'Brian Sam Alice','Sam Alice','Samuel Alice','Alice Sam Brian','Sam Brian','Samuel Brian',
        #                                                     'Alice Esam','Brian Esam'])

        #self.assertEquals(db.calculate_searchPartName("sam"),['Alice Sam','Brian Sam','Alice Sammer','Brian Sammer','Alice Samming','Brian Samming',
        #                                                    'Sam Alice','Sam Brian','Samuel Alice','Samuel Brian'])
        #self.assertEquals(db.calculate_searchPartName("sam"),['Alice Sam','Brian Sam','Alice Sammer','Brian Sammer','Alice Samming','Brian Samming',
        #                                                    'Sam Alice','Sam Brian','Samuel Alice','Samuel Brian','Brian Sam Alice','Alice Sam Brian'])
        self.assertEquals(db.calculate_searchPartName("sam"),['Alice Sam','Brian Sam','Alice Sammer','Brian Sammer','Alice Samming','Brian Samming',
                                                            'Sam Alice','Sam Brian','Samuel Alice','Samuel Brian','Brian Sam Alice','Alice Sam Brian','Alice Esam','Brian Esam'])
        self.assertTrue(db.read(path.join(self.data_dir, "sprint3_final.xml")))
        self.assertEquals(db.calculate_searchPartName("sam"),['Alice Sam','Brian Sam','Alice Sammer','Brian Sammer','Alice Samming','Brian Samming',
                                                            'Sam Alice','Sam Brian','Samuel Alice','Samuel Brian','Brian Sam Alice','Alice Sam Brian','Alice Esam','Brian Esam','Esam Alice','Esam Brian', 'Brian Esam Alice', 'Alice Esam Brian'])

if __name__ == '__main__':
    unittest.main()
