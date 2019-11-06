import factory
from django.contrib.auth.models import User


class UseTestDatabaseFactory(factory.DjangoModelFactory):

    @classmethod
    def _get_manager(cls, model_class):
        manager = super(UseTestDatabaseFactory, cls)._get_manager(model_class)
        return manager.using('test')


class UserFactory(UseTestDatabaseFactory):
    class Meta:
        model = User
        database = "test"

    first_name = 'Brendon'
    last_name = 'Lam'
    username = "blam"
