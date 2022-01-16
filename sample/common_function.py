from msilib.schema import ListBox
from typing import List
from xmlrpc.client import Boolean
from sample.hero import Hero
from sample.team import Team
import sample.common_const as HeroConst

from sqlmodel import SQLModel, Session, create_engine, delete
from logging import getLogger, StreamHandler, DEBUG
import traceback
import sqlalchemy
from sqlalchemy.future import Engine
from sqlalchemy.orm import sessionmaker

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


def delete_all() -> Boolean:
    engine = get_engine()

    with create_session(engine) as session:
        try:
            statement_hero = delete(Hero)
            delete_hero_result = session.exec(statement_hero)

            statement_team = delete(Team)
            delete_team_result = session.exec(statement_team)

            session.commit()
            logger.debug(f"delete_hero_result.rowcount={delete_hero_result.rowcount}")
            logger.debug(f"delete_team_result.rowcount={delete_team_result.rowcount}")
        except (sqlalchemy.exc.OperationalError, BaseException) as error:
            # テーブルが存在しないときにsqlalchemy.exc.OperationalErrorが発生するが問題問題なし
            if type(error) == sqlalchemy.exc.OperationalError:
                logger.error(f"Exception occurred")
                return True

            trace = traceback.format_exception_only(type(error), error)
            logger.debug(trace)
            return False

    return True


def init_data() -> List[Hero]:
    logger.debug("init_data start")

    engine = get_engine()

    SQLModel.metadata.create_all(engine)

    teams = generate_initdata_teams()
    heroes = generate_initdata_heroes()

    create_teams(teams, engine)

    # PreventersのidをDeadpondとSpider-Boyのteam_idセット
    heroes[0].team_id = teams[0].id
    heroes[1].team_id = teams[0].id
    # Z-ForceのidをRusty-Manのteam_idセット
    heroes[2].team_id = teams[1].id

    create_heroes(heroes, engine)

    logger.debug("init_data end")

    return heroes


def generate_initdata_teams() -> List[Team]:
    team_preventers = Team(
        name=HeroConst.TEAM_NAME_PREVENTERS, headquarters="Sharp Tower"
    )
    team_z_force = Team(
        name=HeroConst.TEAM_NAME_Z_FORCE, headquarters="Sister Margaret’s Bar"
    )
    return [team_preventers, team_z_force]


def generate_initdata_heroes() -> List[Hero]:
    hero_1 = Hero(
        name=HeroConst.HERO_NAME_DEADPOND,
        secret_name=HeroConst.HERO_SECRET_NAME_DEADPOND,
        age=30,
    )
    hero_2 = Hero(
        name=HeroConst.HERO_NAME_SPIDER_BOY,
        secret_name=HeroConst.HERO_SECRET_NAME_SPIDER_BOY,
    )
    hero_3 = Hero(
        name=HeroConst.HERO_NAME_RUSTY_MAN,
        secret_name=HeroConst.HERO_SECRET_NAME_RUSTY_MAN,
        age=48,
    )
    return [hero_1, hero_2, hero_3]


def create_teams(teams: List[Team], engine: Engine):
    logger.debug(f"create_teams start teams size={len(teams)}")

    with create_session(engine) as session:
        session.add_all(teams)
        session.commit()

        for team in teams:
            # refreshでなくても参照するだけで反映される。アクセスすると同期してくれるっぽい
            session.refresh(team)
            logger.debug(f"team.id={team.id}")

    logger.debug("create_teams end")


def create_heroes(heros: List[Hero], engine: Engine):
    logger.debug(f"create_heroes start heros size={len(heros)}")

    with create_session(engine) as session:
        session.add_all(heros)
        session.commit()

    logger.debug("create_heroes end")


def get_engine() -> Engine:
    return create_engine("sqlite:///database.db", echo=True)


def create_session(engine: Engine) -> Engine:
    return Session(engine)

    """
    session_factory = sessionmaker(
        bind=engine, expire_on_commit=False, autocommit=False
    )

    return session_factory()
    """
