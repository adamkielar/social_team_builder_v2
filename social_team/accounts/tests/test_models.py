from django.test import TestCase
from django.contrib.auth import get_user_model



class ModelTest(TestCase):
    def test_create_user_with_email_success(self):
        """Test creating a new user with email is success"""
        email = 'test@test.pl'
        password = 'testpass'
        user = get_user_model().objects.create_user(email=email,
                                                    password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test the email for a new user
        """
        email = 'test@TEST.PL'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test create a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@test.pl', 'test123')

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

from accounts.models import MainSkill, OtherSkill, UserProject


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