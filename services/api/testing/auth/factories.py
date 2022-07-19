import factory
from auth.models import UserProfile
from auth.utils import pwd_context
from faker import Faker

fake = Faker()


class UserProfileFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserProfile

    id = factory.Sequence(lambda pk: pk)
    email = factory.Sequence(lambda _: fake.email())
    username = fake.user_name()
    is_active = False
    role = UserProfile.RoleEnum.viewer
    password = pwd_context.hash('testing321')
