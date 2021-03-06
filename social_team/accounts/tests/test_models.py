from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import MainSkill, OtherSkill, UserProject


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


class ProfilesModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@test.pl',
            password='testpass'
        )
        self.main_skills = MainSkill.objects.create(name='Python')
        self.other_skills = OtherSkill.objects.create(user=self.user,
                                                      name='Django')

    def test_user_profile_creation(self):
        user = self.user
        user.full_name = 'Jason Bourne'
        user.avatar = SimpleUploadedFile(
            name='sample.png',
            content=open(__file__, 'rb').read(),
            content_type='image/png'
        )
        user.bio = 'I am Jason Bourne'
        user.main_skills.add(self.main_skills)
        user.other_skills.add(self.other_skills)
        user.is_active = True
        user.save()

        self.assertEqual(user.full_name, 'Jason Bourne')
        self.assertEqual(user.avatar.name[:14], 'avatars/sample')
        self.assertEqual(user.bio, 'I am Jason Bourne')
        self.assertEqual(user.main_skills.count(), 1)
        self.assertEqual(user.other_skills.count(), 1)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)

    def test_main_skill_creation(self):
        """Test create main skill"""
        main_skill = 'Python Developer'
        main = MainSkill.objects.create(name=main_skill)

        self.assertEqual(str(main), main_skill)

    def test_other_skill_creation(self):
        """Test create other skill"""
        other_skill = 'AWS'
        other = OtherSkill.objects.create(user=self.user, name=other_skill)

        self.assertEqual(str(other), other_skill)

    def test_user_project_creation(self):
        """Test create user project"""
        project_name = 'Magic'
        url = 'http://www.test.pl'
        user_project = UserProject.objects.create(user=self.user,
                                                  project_name=project_name,
                                                  url=url)

        self.assertEqual(UserProject.objects.all().count(), 1)
