##############
# Don't change
##############

import copy
import typing as tp
from collections import OrderedDict, defaultdict


TEventID = int
THitID = int
TEventRecord = tp.Dict[str, tp.Any]
THitRecord = tp.Dict[str, tp.Any]
TVisitRecord = tp.Dict[str, tp.Any]
TOutputRecord = tp.Dict[str, tp.Any]

OUTPUT_RECORD: TOutputRecord = {
    "HitID": None, "HitTimestamp": None, "SearchQuery": None, "EventID": None,
    "ShowTimestamp": None, "ClickTimestamp": None, "VisitID": None, "VisitTimestamp": None
}

##############


def process_event(
        record:             TEventRecord,
        events_storage:     tp.Dict[TEventID, TEventRecord],
        hit_events_index:   tp.Dict[THitID, tp.List[TEventID]],
        hit_storage:        tp.Dict[THitID, THitRecord],
        event_visit_buffer: tp.OrderedDict[TEventID, TVisitRecord],
        is_click:           bool = False
        ) -> None:
    """
    Save event to events_storage and join hit from hit_storage and visit from event_visit_buffer if exists
    """


def process_hit(
        record:             THitRecord,
        hit_storage:        tp.Dict[THitID, THitRecord],
        hit_events_index:   tp.Dict[THitID, tp.List[TEventID]],
        events_storage:     tp.Dict[TEventID, TEventRecord],
        ) -> None:
    """
    Store hit in hit_storage and join it for events which are already in events_storage
    """


def process_visit(
        record:              TVisitRecord,
        events_storage:      tp.Dict[TEventID, TEventRecord],
        event_visit_buffer:  tp.OrderedDict[TEventID, TVisitRecord]
        ) -> None:
    """
    Join visit to event in events_storage or store it in event_visit_buffer for future join
    """


###############
# Don't change
###############


def join(
        records: tp.List[tp.Union[TEventRecord, TVisitRecord, THitRecord]]
        ) -> tp.Iterable[TOutputRecord]:

    events_storage: tp.Dict[TEventID, TEventRecord] = {}

    hit_storage: tp.Dict[THitID, THitRecord] = {}

    # Limited buffer by 3 items of visits
    event_visit_buffer: tp.OrderedDict[TEventID, TVisitRecord] = OrderedDict()

    hit_events_index: tp.Dict[THitID, tp.List[TEventID]] = defaultdict(list)

    for record in records:
        if record["EventType"] == "show":
            process_event(record, events_storage, hit_events_index, hit_storage, event_visit_buffer, is_click=False)
        if record["EventType"] == "click":
            process_event(record, events_storage, hit_events_index, hit_storage, event_visit_buffer, is_click=True)
        if record["EventType"] == "hit":
            process_hit(record, hit_storage, hit_events_index, events_storage)
        if record["EventType"] == "visit":
            process_visit(record, events_storage, event_visit_buffer)

    return events_storage.values()


###############
