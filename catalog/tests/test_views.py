from django.test import TestCase
from django.urls import reverse

from catalog.models import Author


class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create 13 authors for pagination tests
        number_of_authors = 13
        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Christian {author_id}',
                last_name=f'Surname {author_id}'
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_is_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/authors.html')

    def test_pagination_is_2(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        # self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['authors']), 2)

    def test_list_of_all_authors(self):
        response = self.client.get(reverse('authors') + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        # self.assertEqual(len(response.context['authors']),3)
        print(response.context)