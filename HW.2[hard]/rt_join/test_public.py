import copy
import dataclasses
import itertools

import typing as tp
import pytest


from . import rt_join as rt_join


hit_record = {"EventType": "hit", "HitID": None, "Timestamp": None, "SearchQuery": None}
event_record = {"EventType": "show", "HitID": None, "EventID": None, "Timestamp": None}
visit_record = {"EventType": "visit", "VisitID": None, "EventID": None, "Timestamp": None}


@dataclasses.dataclass
class Case:
    name:                 str
    given:                tp.List[rt_join.TOutputRecord]
    expected:             tp.List[rt_join.TOutputRecord]
    preserve_given_order: bool = False

    def __str__(self) -> str:
        return 'join_{}'.format(self.name)


TEST_CASES = [
    Case(
        name="hit_with_multiple_shows",
        given=[
            {"EventType": "hit", "HitID": 1, "Timestamp": 10, "SearchQuery": "купить слона"},
            {"EventType": "show", "HitID": 1, "EventID": 1, "Timestamp": 11},
            {"EventType": "show", "HitID": 1, "EventID": 2, "Timestamp": 12},
            {"EventType": "show", "HitID": 1, "EventID": 3, "Timestamp": 13},
        ],
        expected=[
            {"HitID": 1, "HitTimestamp": 10, "SearchQuery": "купить слона", "EventID": 1,
                "ShowTimestamp": 11, "ClickTimestamp": None, "VisitID": None, "VisitTimestamp": None},
            {"HitID": 1, "HitTimestamp": 10, "SearchQuery": "купить слона", "EventID": 2,
             "ShowTimestamp": 12, "ClickTimestamp": None, "VisitID": None, "VisitTimestamp": None},
            {"HitID": 1, "HitTimestamp": 10, "SearchQuery": "купить слона", "EventID": 3,
             "ShowTimestamp": 13, "ClickTimestamp": None, "VisitID": None, "VisitTimestamp": None}
        ]),
    Case(
        name="hit_ended_with_visit",
        given=[
            {"EventType": "hit", "HitID": 3, "Timestamp": 13, "SearchQuery": "суши в москве"},
            {"EventType": "show", "HitID": 3, "EventID": 7, "Timestamp": 18},
            {"EventType": "show", "HitID": 3, "EventID": 6, "Timestamp": 18},
            {"EventType": "click", "HitID": 3, "EventID": 6, "Timestamp": 25},
            {"EventType": "visit", "VisitID": 1, "EventID": 6, "Timestamp": 26},
        ],
        expected=[
            {"HitID": 3, "HitTimestamp": 13, "SearchQuery": "суши в москве", "EventID": 6,
             "ShowTimestamp": 18, "ClickTimestamp": 25, "VisitID": 1, "VisitTimestamp": 26},
            {"HitID": 3, "HitTimestamp": 13, "SearchQuery": "суши в москве", "EventID": 7,
             "ShowTimestamp": 18, "ClickTimestamp": None, "VisitID": None, "VisitTimestamp": None},
        ]),
    Case(
        name="loosed_hit",
        given=[
            {"EventType": "show", "HitID": 3, "EventID": 7, "Timestamp": 18},
            {"EventType": "show", "HitID": 3, "EventID": 6, "Timestamp": 18},
            {"EventType": "click", "HitID": 3, "EventID": 6, "Timestamp": 25},
            {"EventType": "visit", "VisitID": 1, "EventID": 6, "Timestamp": 26},
        ],
        expected=[
            {"HitID": 3, "HitTimestamp": None, "SearchQuery": None, "EventID": 6,
             "ShowTimestamp": 18, "ClickTimestamp": 25, "VisitID": 1, "VisitTimestamp": 26},
            {"HitID": 3, "HitTimestamp": None, "SearchQuery": None, "EventID": 7,
             "ShowTimestamp": 18, "ClickTimestamp": None, "VisitID": None, "VisitTimestamp": None},
        ]),
    Case(
        name="loosed_click",
        given=[
            {"EventType": "hit", "HitID": 3, "Timestamp": 13, "SearchQuery": "суши в москве"},
            {"EventType": "show", "HitID": 3, "EventID": 7, "Timestamp": 18},
            {"EventType": "show", "HitID": 3, "EventID": 6, "Timestamp": 18},
            {"EventType": "visit", "VisitID": 1, "EventID": 6, "Timestamp": 26},
        ],
        expected=[
            {"HitID": 3, "HitTimestamp": 13, "SearchQuery": "суши в москве", "EventID": 6,
             "ShowTimestamp": 18, "ClickTimestamp": None, "VisitID": 1, "VisitTimestamp": 26},
            {"HitID": 3, "HitTimestamp": 13, "SearchQuery": "суши в москве", "EventID": 7,
             "ShowTimestamp": 18, "ClickTimestamp": None, "VisitID": None, "VisitTimestamp": None},
        ]),
    Case(
        name="multiple_clicks",
        given=[
            {"EventType": "hit", "HitID": 3, "Timestamp": 13, "SearchQuery": "суши в москве"},
            {"EventType": "show", "HitID": 3, "EventID": 7, "Timestamp": 18},
            {"EventType": "show", "HitID": 3, "EventID": 6, "Timestamp": 18},
            {"EventType": "click", "HitID": 3, "EventID": 6, "Timestamp": 25},
            {"EventType": "visit", "VisitID": 1, "EventID": 6, "Timestamp": 26},
            {"EventType": "click", "HitID": 3, "EventID": 7, "Timestamp": 29},
            {"EventType": "visit", "VisitID": 2, "EventID": 7, "Timestamp": 32},

        ],
        expected=[
            {"HitID": 3, "HitTimestamp": 13, "SearchQuery": "суши в москве", "EventID": 6,
             "ShowTimestamp": 18, "ClickTimestamp": 25, "VisitID": 1, "VisitTimestamp": 26},
            {"HitID": 3, "HitTimestamp": 13, "SearchQuery": "суши в москве", "EventID": 7,
             "ShowTimestamp": 18, "ClickTimestamp": 29, "VisitID": 2, "VisitTimestamp": 32},
        ]),
    Case(
        name="multiple_hits_with_lost_events",
        given=[
            {"EventType": "hit", "HitID": 21, "Timestamp": 64, "SearchQuery": "Как приготовить доширак"},
            {"EventType": "show", "HitID": 21, "EventID": 29, "Timestamp": 65},
            {"EventType": "click", "HitID": 21, "EventID": 31, "Timestamp": 66},
            {"EventType": "hit", "HitID": 15, "Timestamp": 55, "SearchQuery": "Смотреть сериалы онлайн бесплатно"},
            {"EventType": "hit", "HitID": 3, "Timestamp": 13, "SearchQuery": "суши в москве"},
            {"EventType": "show", "HitID": 3, "EventID": 7, "Timestamp": 18},
            {"EventType": "visit", "VisitID": 1, "EventID": 6, "Timestamp": 26},
            {"EventType": "click", "HitID": 3, "EventID": 7, "Timestamp": 29},
        ],
        expected=[
            {"HitID": 3, "HitTimestamp": 13, "SearchQuery": "суши в москве", "EventID": 7,
             "ShowTimestamp": 18, "ClickTimestamp": 29, "VisitID": None, "VisitTimestamp": None},
            {"HitID": 21, "HitTimestamp": 64, "SearchQuery": "Как приготовить доширак", "EventID": 29,
             "ShowTimestamp": 65, "ClickTimestamp": None, "VisitID": None, "VisitTimestamp": None},
            {"HitID": 21, "HitTimestamp": 64, "SearchQuery": "Как приготовить доширак", "EventID": 31,
             "ShowTimestamp": None, "ClickTimestamp": 66, "VisitID": None, "VisitTimestamp": None},
        ]),
    Case(
        name="throw_out_visits",
        given=[
            # Показывающие машинки залипли и доехали только логи метрики
            {"EventType": "visit", "VisitID": 3, "EventID": 8, "Timestamp": 38},
            {"EventType": "visit", "VisitID": 4, "EventID": 9, "Timestamp": 41},
            {"EventType": "visit", "VisitID": 5, "EventID": 29, "Timestamp": 66},
            {"EventType": "visit", "VisitID": 1, "EventID": 6, "Timestamp": 26},
            {"EventType": "visit", "VisitID": 2, "EventID": 7, "Timestamp": 32},

            # Теряем визиты из буффера
            {"EventType": "hit", "HitID": 21, "Timestamp": 64, "SearchQuery": "Как приготовить доширак"},
            {"EventType": "show", "HitID": 21, "EventID": 29, "Timestamp": 65},
            {"EventType": "show", "HitID": 21, "EventID": 30, "Timestamp": 65},
            {"EventType": "show", "HitID": 21, "EventID": 31, "Timestamp": 65},
            {"EventType": "click", "HitID": 21, "EventID": 31, "Timestamp": 66},
            {"EventType": "click", "HitID": 21, "EventID": 30, "Timestamp": 70},
            {"EventType": "click", "HitID": 21, "EventID": 29, "Timestamp": 79},
            {"EventType": "hit", "HitID": 15, "Timestamp": 55, "SearchQuery": "Смотреть сериалы онлайн бесплатно"},
            {"EventType": "hit", "HitID": 3, "Timestamp": 13, "SearchQuery": "суши в москве"},
            {"EventType": "show", "HitID": 3, "EventID": 7, "Timestamp": 18},
            {"EventType": "show", "HitID": 3, "EventID": 6, "Timestamp": 18},
            {"EventType": "show", "HitID": 3, "EventID": 8, "Timestamp": 18},
            {"EventType": "show", "HitID": 3, "EventID": 9, "Timestamp": 18},
            {"EventType": "click", "HitID": 3, "EventID": 6, "Timestamp": 25},
            {"EventType": "click", "HitID": 3, "EventID": 7, "Timestamp": 29},
            {"EventType": "click", "HitID": 3, "EventID": 8, "Timestamp": 35},
            {"EventType": "click", "HitID": 3, "EventID": 9, "Timestamp": 39},
        ],
        expected=[
            {"HitID": 3, "HitTimestamp": 13, "SearchQuery": "суши в москве", "EventID": 6,
             "ShowTimestamp": 18, "ClickTimestamp": 25, "VisitID": 1, "VisitTimestamp": 26},
            {"HitID": 3, "HitTimestamp": 13, "SearchQuery": "суши в москве", "EventID": 7,
             "ShowTimestamp": 18, "ClickTimestamp": 29, "VisitID": 2, "VisitTimestamp": 32},
            {"HitID": 3, "HitTimestamp": 13, "SearchQuery": "суши в москве", "EventID": 8,
             "ShowTimestamp": 18, "ClickTimestamp": 35, "VisitID": None, "VisitTimestamp": None},
            {"HitID": 3, "HitTimestamp": 13, "SearchQuery": "суши в москве", "EventID": 9,
             "ShowTimestamp": 18, "ClickTimestamp": 39, "VisitID": None, "VisitTimestamp": None},
            {"HitID": 21, "HitTimestamp": 64, "SearchQuery": "Как приготовить доширак", "EventID": 29,
             "ShowTimestamp": 65, "ClickTimestamp": 79, "VisitID": 5, "VisitTimestamp": 66},
            {"HitID": 21, "HitTimestamp": 64, "SearchQuery": "Как приготовить доширак", "EventID": 30,
             "ShowTimestamp": 65, "ClickTimestamp": 70, "VisitID": None, "VisitTimestamp": None},
            {"HitID": 21, "HitTimestamp": 64, "SearchQuery": "Как приготовить доширак", "EventID": 31,
             "ShowTimestamp": 65, "ClickTimestamp": 66, "VisitID": None, "VisitTimestamp": None},
        ],
        preserve_given_order=True)
]


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_only_shows_records(t: Case) -> None:

    expected = sorted(t.expected, key=lambda x: x['EventID'])

    if not t.preserve_given_order:
        for perm in itertools.permutations(t.given):
            records = list(perm)

            given_copied = copy.deepcopy(records)
            assert sorted(rt_join.join(given_copied), key=lambda x: x['EventID']) == expected
            assert given_copied == records, "You shouldn't change inputs"
    else:
        given_copied = copy.deepcopy(t.given)
        assert sorted(rt_join.join(given_copied), key=lambda x: x['EventID']) == expected
