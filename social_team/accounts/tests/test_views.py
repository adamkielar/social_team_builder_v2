from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import User, UserProject


class ProfilePageView(TestCase):
    def setUp(self):
        self.client = Client()
        email = 'test@test.pl'
        password = 'testpass'
        full_name = 'Jason Bourne'
        bio = 'I am Jason Bourne'
        self.user = User.objects.create(email=email,
                                        password=password,
                                        full_name=full_name,
                                        bio=bio)

        project_name = 'Magic'
        url = 'http://www.test.pl'
        self.user_project = UserProject.objects.create(user=self.user,
                                                       project_name=project_name,
                                                       url=url)

    def test_profile_detail_view(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('accounts:profile_detail', kwargs={'pk': self.user.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(self.user, resp.context)
        self.assertTemplateUsed(resp, 'accounts/profile.html')
        self.assertIn(self.user_project, resp.context['user_projects'])

    def test_profile_update_view(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('accounts:profile_edit', kwargs={'pk': self.user.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'accounts/profile_form.html')
