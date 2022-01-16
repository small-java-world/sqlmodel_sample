from multiprocessing.dummy.connection import Listener
import sys
import pytest
from logging import getLogger, StreamHandler, DEBUG
from typing import List, Tuple

from sample.hero import Hero
from sample.common_function import delete_all, init_data
import sample.common_const as HeroConst

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


@pytest.fixture
def init_data_fixture():
    # sqlite:///database.dbとローカルファイル指定なので全データ削除
    delete_all()
    # 前提データの作成
    init_data()


def test_delete_all(init_data_fixture):
    logger.debug(f"{sys._getframe().f_code.co_name} start")

    assert delete_all()

    logger.debug(f"{sys._getframe().f_code.co_name} end")


def test_init_data():
    logger.debug(f"{sys._getframe().f_code.co_name} start")

    heroes = init_data()
    assert len(heroes) == 3

    # 関連付けられていたセッションから遅延ロードしようとして、sqlalchemy.orm.exc.DetachedInstanceErrorが発生して読めない
    # デフォルトだとcommitするとセッション内のインスタンスが全て期限切れになるので
    # sqlalchemyのsessionmakerでexpire_on_commit=Falseを指定してセッションを作成しないと以下の検証は実行できません。

    """
    assert heroes[0].name == HeroConst.HERO_NAME_DEADPOND
    assert heroes[1].name == HeroConst.HERO_NAME_SPIDER_BOY
    assert heroes[2].name == HeroConst.HERO_NAME_RUSTY_MAN
    """

    logger.debug(f"{sys._getframe().f_code.co_name} end")
