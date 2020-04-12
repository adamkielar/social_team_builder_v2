import unittest

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client, TestCase

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
    def test_home_view_render(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'index.html')