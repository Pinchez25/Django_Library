from django.shortcuts import get_object_or_404
from django.test import TestCase
from catalog.models import Author

"""
    setUpTestData() - called once at the beginning of the test run for
         class-level setup. You'd use this to create objects that aren't going to
         be modified or changed in any of the test methods.
         
    setUp() - called before every test function to set up any objects that may be
        modified by the test (every test function will get a 'fresh' version of these objects).
        
    tearDown() - not particularly useful for database tests, since the TestCase base class takes
         care of the database teardown for you.
         
    Assert functions - AssertTrue, AssertFalse and AssertEqual
    
    There are django specific assertions eg.
    1. assertRedirects - test if a view redirects
    2. assertTemplateUsed - test if a particular view has been used
    
    Run tests: python manage.py test
    
    Get more info about a test: py manage.py test --verbosity 2 (verbosity levels allowed are 0,1(default),2,3
    
    Run specific tests:
         py manage.py test catalog.tests  // test specified module
         py manage.py test catalog.tests.test_models // test specified module
         py manage.py test catalog.tests.test_models.YourTestClass // test specified class
         py manage.py test catalog.tests.test_models.YourTestClass.test_one_plus_one_equals_two // test specified method

"""


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name='John', last_name='Kerry')

    def test_first_name_label(self):
        author = get_object_or_404(Author, pk=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'died')

    def test_first_name_max_length(self):
        author = get_object_or_404(Author, pk=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_first_name_space_last_name(self):
        author = get_object_or_404(Author, pk=1)
        expected_object_name = f'{author.first_name} {author.last_name}'
        self.assertEqual(str(author), expected_object_name)

    def test_get_absolute_url(self):
        author = get_object_or_404(Author, pk=1)
        # will fail if urlconf is not defined
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1')
