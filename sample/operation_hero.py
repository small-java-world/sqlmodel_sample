from msilib.schema import ListBox
from typing import List
from sample.hero import Hero
from sample.team import Team
from sample.common_function import get_engine, create_session

from sqlmodel import (
    Field,
    Session,
    SQLModel,
    create_engine,
    select,
    or_,
)

from logging import exception, getLogger, StreamHandler, DEBUG

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


def select_all() -> List[Hero]:
    engine = get_engine()

    with create_session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes


def select_by_name(name: str) -> List[Hero]:
    engine = get_engine()

    with create_session(engine) as session:
        statement = select(Hero).where(Hero.name == name)
        return session.exec(statement).all()


def select_by_name_and_secret_name(name: str, secret_name: str) -> List[Hero]:
    engine = get_engine()

    with create_session(engine) as session:
        statement = (
            select(Hero).where(Hero.name == name).where(Hero.secret_name == secret_name)
        )

        # 単一のwhereでも指定可能
        # statement = select(Hero).where(Hero.name == name, Hero.secret_name == secret_name)

        return session.exec(statement).all()


def select_by_name_or_secret_name(name: str, secret_name: str) -> List[Hero]:
    engine = get_engine()

    with create_session(engine) as session:
        statement = select(Hero).where(
            or_(Hero.name == name, Hero.secret_name == secret_name)
        )
        return session.exec(statement).all()


def select_by_age_above(age: int) -> List[Hero]:
    engine = get_engine()

    with create_session(engine) as session:
        statement = select(Hero).where(Hero.age > age)
        return session.exec(statement).all()


def update_age_by_name(name: str, age: int) -> List[Hero]:
    engine = get_engine()
    with create_session(engine) as session:
        statement = select(Hero).where(Hero.name == name)
        hero = session.exec(statement).one()

        # heroインスタンスのageを更新してsession.addとsession.commitで更新
        hero.age = age
        session.add(hero)
        session.commit()
