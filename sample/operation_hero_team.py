from msilib.schema import ListBox
from typing import List
from sample.hero import Hero
from sample.team import Team

from sqlmodel import Field, Session, SQLModel, create_engine, select, delete, or_
from logging import getLogger, StreamHandler, DEBUG

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


def init_data():
    logger.debug("init_data start")

    team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
    team_z_force = Team(name="Z-Force", headquarters="Sister Margaret’s Bar")

    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson", age=30)
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    create_teams([team_preventers, team_z_force])

    hero_1.team_id = team_preventers.id
    hero_2.team_id = team_preventers.id
    hero_3.team_id = team_z_force.id

    create_heroes([hero_1, hero_2, hero_3])

    logger.debug("init_data end")


def create_teams(teams: List[Team]):
    logger.debug(f"create_teams start teams size={len(teams)}")

    engine = get_engine()

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add_all(teams)
        session.commit()

        for team in teams:
            # refreshでなくても参照するだけで反映される。アクセスすると同期してくれるっぽい
            session.refresh(team)
            logger.debug(f"team.id={team.id}")

    logger.debug("create_teams end")


def create_heroes(heros: List[Hero]):
    logger.debug(f"create_heroes start heros size={len(heros)}")

    engine = get_engine()

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add_all(heros)
        session.commit()

    logger.debug("create_heroes end")


def delete_all() -> None:
    engine = get_engine()

    with Session(engine) as session:
        statement_hero = delete(Hero)
        delete_hero_result = session.exec(statement_hero)

        statement_team = delete(Team)
        delete_team_result = session.exec(statement_team)

        session.commit()
        logger.debug(f"delete_hero_result.rowcount={delete_hero_result.rowcount}")
        logger.debug(f"delete_team_result.rowcount={delete_team_result.rowcount}")


def select_heroes_by_team_name(team_name: str) -> List[Hero]:
    engine = get_engine()

    with Session(engine) as session:
        statement = select(Hero, Team).where(
            Hero.team_id == Team.id, Team.name == team_name
        )
        return session.exec(statement).all()


def get_engine():
    return create_engine("sqlite:///database.db", echo=True)
