"""Test fixtures: restore the in-memory store to a clean seed before each test.

The mock store (data_store.ORDERS / ACCOUNT / INVESTIGATIONS) is mutated in
place by the tools, so tests must reset it or state bleeds between them.
"""

import copy

import pytest

from marketplace_support_agent import data_store

_PRISTINE_ORDERS = copy.deepcopy(data_store.ORDERS)
_PRISTINE_ACCOUNT = copy.deepcopy(data_store.ACCOUNT)


@pytest.fixture(autouse=True)
def reset_store():
    data_store.ORDERS.clear()
    data_store.ORDERS.update(copy.deepcopy(_PRISTINE_ORDERS))
    data_store.ACCOUNT.clear()
    data_store.ACCOUNT.update(copy.deepcopy(_PRISTINE_ACCOUNT))
    data_store.INVESTIGATIONS.clear()
    yield
