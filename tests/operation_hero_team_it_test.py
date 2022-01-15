from multiprocessing.dummy.connection import Listener
import sys
import pytest
from logging import getLogger, StreamHandler, DEBUG
from typing import List, Tuple

from sample.operation_hero_team import (
    init_data,
    delete_all,
    select_heroes_by_team_name,
)
from sample.hero import Hero

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


@pytest.fixture
def init_data_fixture():
    delete_all()
    init_data()


def test_select_heroes_by_team_name(init_data_fixture):
    logger.debug(f"{sys._getframe().f_code.co_name} start")

    result = select_heroes_by_team_name("Preventers")
    assert len(result) == 2

    result = select_heroes_by_team_name("Z-Force")
    assert len(result) == 1

    logger.debug(f"{sys._getframe().f_code.co_name} end")
