import factory
from faker import Faker
from users.database import models
from users.schemas.enums import LibraryTypeEnum

fake = Faker()


class UserLibraryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.UserLibrary
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda pk: pk)
    object = factory.SubFactory('tests.content.factories.MovieFactory')
    user_id = fake.pyint(min_value=1, max_value=100)
    library_type = LibraryTypeEnum.favorite
    offset = fake.pyint(min_value=0, max_value=100)
