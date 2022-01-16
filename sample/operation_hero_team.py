from msilib.schema import ListBox
from typing import List
from sample.hero import Hero
from sample.team import Team
from sample.common_function import get_engine, create_session

from sqlmodel import Field, Session, SQLModel, create_engine, select, delete, or_
from logging import getLogger, StreamHandler, DEBUG
from sqlalchemy.orm.session import sessionmaker

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


def select_heroes_by_team_name(team_name: str) -> List[Hero]:
    engine = get_engine()

    with create_session(engine) as session:
        statement = select(Hero, Team).where(
            Hero.team_id == Team.id, Team.name == team_name
        )
        return session.exec(statement).all()
