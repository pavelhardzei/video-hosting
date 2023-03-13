import factory
from faker import Faker
from tests.content.factories import MovieFactory
from users.database import models
from users.schemas import enums

fake = Faker()


class UserLibraryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.UserLibrary
        sqlalchemy_session_persistence = 'commit'

    user_id = fake.pyint(min_value=1, max_value=100)
    library_type = enums.LibraryTypeEnum.favorite
    offset = fake.pyint(min_value=0, max_value=100)

    object_type = enums.UserLibraryObjectEnum.movie
    object_id = 1

    @factory.post_generation
    def create_object(self, create, value, **kwargs):
        self.object = MovieFactory()
        self.save()
