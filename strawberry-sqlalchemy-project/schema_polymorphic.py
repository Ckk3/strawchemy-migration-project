"""
STRAWBERRY-SQLALCHEMY-MAPPER EXCLUSIVE FEATURE: Polymorphic Type Hierarchies

This feature is NOT available in strawchemy (not documented).

Use @mapper.interface for the base model and @mapper.type for children
to automatically map SQLAlchemy polymorphic models to GraphQL interfaces.
"""

from typing import List
import strawberry
from strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyMapper
from sqlalchemy import select, String, Column

import models
from database import Base, get_session


# SQLAlchemy single-table inheritance with 'type' as discriminator
class Content(Base):
    __tablename__ = "content"

    id = Column(String(36), primary_key=True)
    title = Column(String(200), nullable=False)
    body = Column(String, nullable=True)
    type = Column(String(50), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "content",
        "polymorphic_on": type,
    }


class Article(Content):
    author = Column(String(100), nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "article",
    }


class Video(Content):
    duration_seconds = Column(String(50), nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "video",
    }


strawberry_sqlalchemy_mapper = StrawberrySQLAlchemyMapper()


# @interface for the base model creates a GraphQL interface
@strawberry_sqlalchemy_mapper.interface(Content)
class ContentInterface:
    pass


# @type for child models creates implementing types
@strawberry_sqlalchemy_mapper.type(Article)
class ArticleType:
    pass


@strawberry_sqlalchemy_mapper.type(Video)
class VideoType:
    pass


@strawberry.type
class QueryWithPolymorphic:
    @strawberry.field
    def all_content(self) -> List[ContentInterface]:
        session = get_session()
        return list(session.scalars(select(Content)).all())

    @strawberry.field
    def articles(self) -> List[ArticleType]:
        session = get_session()
        return list(session.scalars(select(Article)).all())

    @strawberry.field
    def videos(self) -> List[VideoType]:
        session = get_session()
        return list(session.scalars(select(Video)).all())


strawberry_sqlalchemy_mapper.finalize()
additional_types = list(strawberry_sqlalchemy_mapper.mapped_types.values())

schema_with_polymorphic = strawberry.Schema(
    query=QueryWithPolymorphic,
    types=additional_types,
)
