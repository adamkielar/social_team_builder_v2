from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import MainSkill, OtherSkill
from projects.models import Project, Position, Applicant


class ProjectsModelsTest(TestCase):
    def setUp(self):
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
            project_status='OPEN'
        )
        self.position = Position.objects.create(
            project=self.project,
            title='Haskell Developer',
            description='testing',
            position_status='APPLY'
        )

    def test_project_creation(self):
        """Test creation Project model"""
        self.user = get_user_model().objects.get(id=1)
        project = Project.objects.create(
            owner=self.user,
            title='Calculator',
            description='app',
            project_timeline='2 months',
            applicant_requirements='PHP',
            project_status='OPEN'
        )

        self.assertEqual(str(project.title), 'Calculator')
        self.assertEqual(Project.objects.all().count(), 2)

    def test_position_creation(self):
        """Test creation of Position model"""
        position = Position.objects.create(
            project=self.project,
            title='Python Developer',
            description='testing',
            position_status='APPLY'
        )
        position.main_skills.add(1)
        position.other_skills.add(1)
        position.save()

        self.assertEqual(str(position.title), 'Python Developer')
        self.assertEqual(Position.objects.all().count(), 2)

    def test_applicant_creation(self):
        """Test creation of Applicant model"""
        applicant = Applicant.objects.create(
            user_profile=self.user,
            project=self.project,
            position=self.position,
            applicant_status='APPROVED'
        )

        self.assertEqual(Applicant.objects.all().count(), 1)
