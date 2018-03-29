# coding: utf-8
import logging

log = logging.getLogger(__name__)


def make_desision1(acts):
    # log.debug('acts=%s', acts)  # todo log
    d = {}
    for act, weight in acts:
        d[act] = d.get(act, 0) + weight
    acts2 = [(act, weight) for act, weight in d.items()]
    acts2.sort(key=lambda x: -x[1])
    # log.info(acts2)

    acts3 = filter(lambda x: x[1] > 0, acts2)
    # log.info(acts3)
    return acts3
