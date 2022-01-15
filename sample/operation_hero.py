from msilib.schema import ListBox
from typing import List
from sample.hero import Hero
from sample.team import Team

from sqlmodel import (
    Field,
    Session,
    SQLModel,
    create_engine,
    select,
    delete,
    or_,
    update,
)

from logging import getLogger, StreamHandler, DEBUG

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


def init_data():
    logger.debug("init_data start")

    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson", age=30)
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    create([hero_1, hero_2, hero_3])

    logger.debug("init_data end")


def create(target_list: List[Hero]):
    logger.debug(f"create start target_list size={len(target_list)}")

    engine = get_engine()

    logger.debug("create_all start")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add_all(target_list)
        session.commit()

    logger.debug("create end")


def select_all() -> List[Hero]:
    engine = get_engine()

    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes


def select_by_name(name: str) -> List[Hero]:
    engine = get_engine()

    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == name)
        return session.exec(statement).all()


def select_by_name_and_secret_name(name: str, secret_name: str) -> List[Hero]:
    engine = get_engine()

    with Session(engine) as session:
        statement = (
            select(Hero).where(Hero.name == name).where(Hero.secret_name == secret_name)
        )

        # 単一のwhereでも指定可能
        # statement = select(Hero).where(Hero.name == name, Hero.secret_name == secret_name)

        return session.exec(statement).all()


def select_by_name_or_secret_name(name: str, secret_name: str) -> List[Hero]:
    engine = get_engine()

    with Session(engine) as session:
        statement = select(Hero).where(
            or_(Hero.name == name, Hero.secret_name == secret_name)
        )
        return session.exec(statement).all()


def select_by_age_above(age: int) -> List[Hero]:
    engine = get_engine()

    with Session(engine) as session:
        statement = select(Hero).where(Hero.age > age)
        return session.exec(statement).all()


def delete_all() -> int:
    engine = get_engine()

    with Session(engine) as session:
        statement = delete(Hero)
        delete_result = session.exec(statement)
        session.commit()
        logger.debug(f"delete_result.rowcount={delete_result.rowcount}")

        return delete_result.rowcount


def update_age_by_name(name: str, age: int) -> List[Hero]:
    engine = get_engine()
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == name)
        hero = session.exec(statement).one()

        # heroインスタンスのageを更新してsession.addとsession.commitで更新
        hero.age = age
        session.add(hero)
        session.commit()


def get_engine():
    return create_engine("sqlite:///database.db", echo=True)
