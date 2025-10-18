import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker("name")
    password = factory.PostGenerationMethodCall("set_password", "testpass123")

    # Remove the _create override since it's causing issues
    # @classmethod
    # def _create(cls, model_class, *args, **kwargs):
    #     manager = cls._get_manager(model_class)
    #     return manager.create_user(*args, **kwargs)
