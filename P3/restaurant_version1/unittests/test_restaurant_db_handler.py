'''
Created on May 20, 2015

@author: TomTheToad
'''
import unittest
from mock import patch
from restaurant_version1.restaurant_db_handler import RestaurantDBHandler


class FakeTestObject(object):
    name = 'Test Restaurant'


class Test(unittest.TestCase):

    def setUp(self):
        self.rest_db = RestaurantDBHandler()

    @patch.object(RestaurantDBHandler, 'create_session', autospec=True)
    def test_list_restaurant_names(self, mock_session):

        __list = [FakeTestObject]
        mock_session.return_value.query.return_value.all.return_value = __list

        rest_names_dictionary = self.rest_db.list_restaurants()
        self.assertEqual(rest_names_dictionary, ['Test Restaurant'])

    def test_add_restaurant(self):
        self.rest_db.add_restaurant('Test Restaurant2')

    def test_delete_restaurant(self):
        self.rest_db.delete_restaurants_by_name('Test Restaurant2')

    def test_lookup_restaurant(self):
        self.rest_db.add_restaurant('Test Restaurant3')
        lookup_results = self.rest_db.lookup_restaurant('Test Restaurant3')
        self.rest_db.delete_restaurants_by_name('Test Restaurant3')
        self.assertEqual(lookup_results[0][0], 'Test Restaurant3')

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
