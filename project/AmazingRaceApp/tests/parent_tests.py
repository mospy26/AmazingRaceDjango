from django.contrib.auth.models import User
from django.test import TestCase
from .factory_boy import UserFactory


class DatabaseRequiredTests(TestCase):

    def setUp(self):
        self.user1 = UserFactory(username="blam", password="blam")
