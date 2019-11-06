from django.contrib.auth.models import User

from AmazingRaceApp.tests.parent_tests import DatabaseRequiredTests


class BackendUnitTests(DatabaseRequiredTests):

    def test_example(self):
        user = User.objects.get(username="40wam")
        self.assertEquals(user.username, "40wam", "Incorrect username")