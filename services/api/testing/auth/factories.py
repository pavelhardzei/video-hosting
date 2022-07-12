import factory
from auth import utils
from auth.models import UserProfile, UserSecurity
from faker import Faker

fake = Faker()


class UserProfileFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserProfile
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda pk: pk)
    email = factory.Sequence(lambda _: fake.email())
    username = fake.user_name()
    is_active = False
    role = UserProfile.RoleEnum.viewer
    password = utils.pwd_context.hash('testing321')


class UserSecurityFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserSecurity
        sqlalchemy_session_persistence = 'commit'

    token = None
    email_sent_time = None

    user = factory.SubFactory(UserProfileFactory)
