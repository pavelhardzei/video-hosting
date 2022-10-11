import factory
from auth import utils
from auth.database.models import UserProfile, UserRefreshTokens, UserSecurity
from auth.schemas.enums import RoleEnum
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
    role = RoleEnum.viewer
    password = utils.pwd_context.hash('testing321')


class UserSecurityFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserSecurity
        sqlalchemy_session_persistence = 'commit'

    access_token = None
    email_sent_time = None

    user = factory.SubFactory(UserProfileFactory)


class UserRefreshTokensFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserRefreshTokens
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda pk: pk)
    refresh_token = None

    user = factory.SubFactory(UserProfileFactory)

    @factory.post_generation
    def set_refresh_token(self, create, value, **kwargs):
        self.refresh_token = utils.create_token({'id': self.id, 'user_id': self.user_id})
