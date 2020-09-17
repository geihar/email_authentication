import factory
from .models import db

from src.models import User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    email = factory.Sequence(lambda n: "test%s@example.org" % n)
