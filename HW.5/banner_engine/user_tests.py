import random
import typing

import pytest

from .banner_engine import (
    BannerStat, Banner, BannerStorage, EpsilonGreedyBannerEngine, EmptyBannerStorageError, NoBannerError
)

TEST_DEFAULT_CTR = 0.1


@pytest.fixture(scope="function")
def test_banners() -> typing.List[Banner]:
    return [
        Banner("b1", cost=1, stat=BannerStat(10, 20)),
        Banner("b2", cost=250, stat=BannerStat(20, 20)),
        Banner("b3", cost=100, stat=BannerStat(0, 20)),
        Banner("b4", cost=100, stat=BannerStat(1, 20)),
    ]


@pytest.mark.parametrize("clicks, shows, expected_ctr", [(1, 1, 1.0), (20, 100, 0.2), (5, 100, 0.05)])
def test_banner_stat_ctr_value(clicks: int, shows: int, expected_ctr: float) -> None:
    assert clicks / shows == expected_ctr


BANNER_STAT_LIST = [BannerStat(10), BannerStat(0, 10), BannerStat(100, 0), BannerStat(10, 20), BannerStat()]


def test_empty_stat_compute_ctr_returns_default_ctr() -> None:
    banner_stat = BannerStat()
    assert banner_stat.compute_ctr(TEST_DEFAULT_CTR) == TEST_DEFAULT_CTR


def test_banner_stat_add_show_lowers_ctr() -> None:
    for bs in BANNER_STAT_LIST:
        ctr = bs.compute_ctr(TEST_DEFAULT_CTR)
        bs.add_show()
        assert ctr > bs.compute_ctr(TEST_DEFAULT_CTR) or (ctr == TEST_DEFAULT_CTR and bs.compute_ctr(
            TEST_DEFAULT_CTR) != TEST_DEFAULT_CTR and bs.shows == 1) or not bs.clicks


def test_banner_stat_add_click_increases_ctr() -> None:
    for bs in BANNER_STAT_LIST:
        ctr = bs.compute_ctr(TEST_DEFAULT_CTR)
        bs.add_click()
        assert ctr < bs.compute_ctr(TEST_DEFAULT_CTR) or not bs.shows


def test_get_banner_with_highest_cpc_returns_banner_with_highest_cpc(test_banners: typing.List[Banner]) -> None:
    banner_storage = BannerStorage(test_banners)
    max_ban = test_banners[0]
    for ban in test_banners:
        if max_ban.stat.compute_ctr(TEST_DEFAULT_CTR) < ban.stat.compute_ctr(TEST_DEFAULT_CTR):
            max_ban = ban
    assert banner_storage.banner_with_highest_cpc() == max_ban


def test_banner_engine_raise_empty_storage_exception_if_constructed_with_empty_storage() -> None:
    try:
        ban_eng = EpsilonGreedyBannerEngine(BannerStorage([]), 1.0)
    except EmptyBannerStorageError:
        return
    assert False, f'not raise {EmptyBannerStorageError}'


def test_engine_send_click_not_fails_on_unknown_banner(test_banners: typing.List[Banner]) -> None:
    try:
        ban = EpsilonGreedyBannerEngine(BannerStorage(test_banners), 0.2)
        ban.send_click("b50")
    except all:
        assert False, "Send Click Fails on unknown banner"


def test_engine_with_zero_random_probability_shows_banner_with_highest_cpc(test_banners: typing.List[Banner]) -> None:
    ban = EpsilonGreedyBannerEngine(BannerStorage(test_banners), 0)
    max_ban = test_banners[0]
    for bn in test_banners:
        if max_ban.stat.compute_ctr(TEST_DEFAULT_CTR) < bn.stat.compute_ctr(TEST_DEFAULT_CTR):
            max_ban = bn
    assert ban.show_banner() == max_ban.banner_id


@pytest.mark.parametrize("expected_random_banner", ["b1", "b2", "b3", "b4"])
def test_engine_with_1_random_banner_probability_gets_random_banner(
        expected_random_banner: str,
        test_banners: typing.List[Banner],
        monkeypatch: typing.Any
) -> None:
    def MonkeyRand(arg):
        return expected_random_banner

    monkeypatch.setattr(random, "choice", MonkeyRand)
    ban = EpsilonGreedyBannerEngine(BannerStorage(test_banners), 1)
    assert ban.show_banner() == expected_random_banner


def test_total_cost_equals_to_cost_of_clicked_banners(test_banners: typing.List[Banner]) -> None:
    ban_st = BannerStorage(test_banners)
    total_cost = 0
    ban = EpsilonGreedyBannerEngine(ban_st,0.5)
    for num, el in enumerate(test_banners):
        total_cost += el.stat.clicks * el.cost
        for i in range(num):
            ban.send_click(el.banner_id)
            total_cost += el.cost
    assert ban.total_cost == total_cost


def test_engine_show_increases_banner_show_stat(test_banners: typing.List[Banner]) -> None:
    ban = EpsilonGreedyBannerEngine(BannerStorage(test_banners), 0.75)
    show_stat = ban._show_count
    ban.show_banner()
    assert show_stat == ban._show_count - 1


def test_engine_click_increases_banner_click_stat(test_banners: typing.List[Banner]) -> None:
    ban_st = BannerStorage(test_banners)
    banner = ban_st.get_banner("b1")
    ban_click_stat = banner.stat.clicks
    ban = EpsilonGreedyBannerEngine(BannerStorage(test_banners), 0.75)
    ban.send_click("b1")
    assert ban_click_stat == banner.stat.clicks - 1
