from os import path
import unittest
import comp62521

class TestApp(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        data = ""
        comp62521.app.config['TESTING'] = True
        comp62521.app.config['DATASET'] = data
        comp62521.app.config['DATABASE'] = path.join(dir, "..", "data", data)
        self.app = comp62521.app.test_client()

    def test_averages(self):
        try:
            r = self.app.get("/averages")
            self.assertEqual(200, r.status_code, "Status code was not 'OK'.")
        except AttributeError as error:
            self.assertFalse(True, "Unable to open a /averages with empty data")

if __name__ == '__main__':
    unittest.main()
