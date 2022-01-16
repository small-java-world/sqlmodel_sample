from multiprocessing.dummy.connection import Listener
import sys
import pytest
from logging import getLogger, StreamHandler, DEBUG
from typing import List, Tuple
import sample.common_const as HeroConst

from sample.operation_hero import (
    select_all,
    select_by_name,
    select_by_name_and_secret_name,
    select_by_name_or_secret_name,
    select_by_age_above,
    update_age_by_name,
)
from sample.hero import Hero
from sample.common_function import delete_all, init_data

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


@pytest.fixture(params=[(HeroConst.HERO_NAME_DEADPOND, 1), ("Hoge", 0)])
def test_select_by_name_fixture(request) -> Tuple[str, int]:
    request.getfixturevalue("init_data_fixture")
    return (request.param[0], request.param[1])


def test_select_by_name(test_select_by_name_fixture):
    logger.debug(f"{sys._getframe().f_code.co_name} start")

    name, expected_result = test_select_by_name_fixture

    result = select_by_name(name)
    output_name(result)

    assert len(result) == expected_result

    logger.debug(f"{sys._getframe().f_code.co_name} start")


@pytest.fixture(
    params=[
        (HeroConst.HERO_NAME_DEADPOND, HeroConst.HERO_SECRET_NAME_DEADPOND, 1),
        (HeroConst.HERO_NAME_DEADPOND, HeroConst.HERO_SECRET_NAME_SPIDER_BOY, 0),
        (HeroConst.HERO_NAME_SPIDER_BOY, HeroConst.HERO_SECRET_NAME_DEADPOND, 0),
    ]
)
def test_select_by_name_and_secret_name_fixture(request) -> Tuple[str, str, int]:
    request.getfixturevalue("init_data_fixture")
    return (request.param[0], request.param[1], request.param[2])


def test_select_by_name_and_secret_name(test_select_by_name_and_secret_name_fixture):
    logger.debug(f"{sys._getframe().f_code.co_name} start")

    (
        name,
        secret_name,
        expected_result,
    ) = test_select_by_name_and_secret_name_fixture

    result = select_by_name_and_secret_name(name, secret_name)
    output_name(result)

    assert len(result) == expected_result

    logger.debug(f"{sys._getframe().f_code.co_name} start")


@pytest.fixture(
    params=[
        (HeroConst.HERO_NAME_DEADPOND, HeroConst.HERO_SECRET_NAME_DEADPOND, 1),
        (HeroConst.HERO_NAME_DEADPOND, HeroConst.HERO_SECRET_NAME_SPIDER_BOY, 2),
        (HeroConst.HERO_NAME_SPIDER_BOY, HeroConst.HERO_SECRET_NAME_DEADPOND, 2),
        (HeroConst.HERO_NAME_SPIDER_BOY, "Hoge Hoge", 1),
        ("Hoge", HeroConst.HERO_SECRET_NAME_SPIDER_BOY, 1),
    ]
)
def test_select_by_name_or_secret_name_fixture(request) -> Tuple[str, str, int]:
    request.getfixturevalue("init_data_fixture")
    return (request.param[0], request.param[1], request.param[2])


def test_select_by_name_or_secret_name(test_select_by_name_or_secret_name_fixture):
    logger.debug(f"{sys._getframe().f_code.co_name} start")

    (
        name,
        secret_name,
        expected_result,
    ) = test_select_by_name_or_secret_name_fixture

    result = select_by_name_or_secret_name(name, secret_name)
    output_name(result)

    error_message = (
        f"name={name} secret_name={secret_name}で検索した結果の要素数の期待値は{expected_result}です。"
    )

    assert len(result) == expected_result, error_message

    logger.debug(f"{sys._getframe().f_code.co_name} start")


@pytest.fixture(params=[(29, 2), (30, 1), (47, 1), (48, 0)])
def test_select_by_age_above_fixture(request) -> Tuple[int, int]:
    request.getfixturevalue("init_data_fixture")
    return (request.param[0], request.param[1])


def test_select_by_age_above(test_select_by_age_above_fixture):
    logger.debug(f"{sys._getframe().f_code.co_name} start")

    (
        age,
        expected_result,
    ) = test_select_by_age_above_fixture

    result = select_by_age_above(age)
    output_name(result)

    assert len(result) == expected_result

    logger.debug(f"{sys._getframe().f_code.co_name} start")


def test_select_all(init_data_fixture):
    logger.debug("test_select_all start")

    result = select_all()
    output_name(result)

    assert len(result) == 3

    logger.debug("test_select_all end")


def test_create(init_data_fixture):
    logger.debug(f"{sys._getframe().f_code.co_name} start")

    hero_1 = Hero(name="Hoge", secret_name="Hoge Hoge")
    hero_2 = Hero(name="Fuga", secret_name="Fuga Fuga")

    create([hero_1, hero_2])

    result = select_all()
    output_name(result)

    assert len(result) == 5

    logger.debug(f"{sys._getframe().f_code.co_name} end")


def test_update_age_by_name(init_data_fixture):
    logger.debug(f"{sys._getframe().f_code.co_name} start")

    target_name = "Rusty-Man"
    update_age_by_name(target_name, 50)

    heroes = select_by_name(target_name)

    assert len(heroes) == 1
    assert heroes[0].age == 50

    logger.debug(f"{sys._getframe().f_code.co_name} end")


def output_name(target_list: List[Hero]):
    for index, hero in enumerate(target_list):
        logger.debug(f"index={index} hero.name={hero.name}")
