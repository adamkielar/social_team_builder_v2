from django.urls import reverse
from django.test import Client, TestCase
from django.contrib.auth import get_user_model

from accounts.models import MainSkill, OtherSkill
from projects.models import Project, Position, Applicant


class ProjectPageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        email = 'test@test.pl'
        password = 'testpass'
        self.user = get_user_model().objects.create_user(email=email,
                                                         password=password)
        self.main_skills = MainSkill.objects.create(name='Python')
        self.other_skills = OtherSkill.objects.create(user=self.user, name='Django')

        self.project = Project.objects.create(
            owner=self.user,
            title='Twitter',
            description='app',
            project_timeline='2 months',
            applicant_requirements='PHP',
            project_status='OPEN',
            slug='twitter'
        )

        self.position = Position.objects.create(
            project=self.project,
            title='Haskell Developer',
            description='testing',
            position_status='APPLY'
        )
        self.position.main_skills.add(1)
        self.position.other_skills.add(1)
        self.position.save()

        self.applicant = Applicant.objects.create(
            user_profile=self.user,
            project=self.project,
            position=self.position,
            applicant_status='APPROVED'
        )

    def test_projects_all_view(self):
        resp = self.client.get(reverse('projects:projects_all'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'projects/index.html')

    def test_project_detail_view(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('projects:project_detail', kwargs={'slug': self.project.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'projects/project.html')
        self.assertTrue(self.project, resp.context['object'])

    def test_project_create_view(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('projects:project_new'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'projects/project_form.html')

    def test_project_update_view(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('projects:project_edit', kwargs={'slug': self.project.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'projects/project_edit.html')

    def test_project_delete_view(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('projects:project_delete', kwargs={'slug': self.project.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'projects/project_confirm_delete.html')
        self.assertContains(resp, 'Are you sure you want to delete')

    def test_applicant_list_view(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('projects:applications', kwargs={'pk': self.user.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'projects/applications.html')

    def test_applicant_create_view(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('projects:apply', kwargs={'pk': self.user.id}))
        self.assertRedirects(resp, reverse('projects:projects_all'), fetch_redirect_response=False)

    def test_applicant_updatestatus_view(self):
        self.client.force_login(self.user)
        resp = self.client.get(
            reverse('projects:apply_status', kwargs={'position_pk': self.position.id, 'applicant_pk': self.user.id}))
        self.assertRedirects(resp, reverse('projects:applications', kwargs={'pk': self.user.id}), fetch_redirect_response=False)
