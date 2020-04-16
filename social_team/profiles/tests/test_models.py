from django.test import TestCase
from django.contrib.auth import get_user_model

from profiles.models import MainSkill, OtherSkill, UserProject


class ProfilesModelTest(TestCase):
    def test_main_skill_creation(self):
        """Test create main skill"""
        main_skill = 'Python Developer'
        main = MainSkill.objects.create(main_skill=main_skill)

        self.assertEqual(str(main), main_skill)

    def test_other_skill_creation(self):
        """Test create other skill"""
        other_skill = 'AWS'
        other = OtherSkill.objects.create(other_skill=other_skill)

        self.assertEqual(str(other), other_skill)

    def test_user_project_creation(self):
        """Test create user project"""
        email = 'test@test.pl'
        password = 'testpass'
        user = get_user_model().objects.create_user(email=email,
                                                    password=password)
        project_name = 'Magic'
        url = 'http://www.test.pl'
        user_project = UserProject.objects.create(user=user,
                                                  project_name=project_name,
                                                  url=url)

        self.assertEqual(UserProject.objects.all().count(), 1)