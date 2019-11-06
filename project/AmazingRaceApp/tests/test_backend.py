from AmazingRaceApp.tests.parent_tests import DatabaseRequiredTests


class BackendUnitTests(DatabaseRequiredTests):

    def test_example(self):
        self.assertEquals(self.user1.username, "blam", "Incorrect username")