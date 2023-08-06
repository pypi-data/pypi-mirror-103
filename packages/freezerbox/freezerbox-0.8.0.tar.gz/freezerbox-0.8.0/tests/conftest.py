#!/usr/bin/env python3

import pytest
import freezerbox

from freezerbox.stepwise.make import StepwiseMaker, OrderMaker
from mock_model import MockSoloMaker, MockComboMaker

class MockEntryPoint:

    def __init__(self, plugin):
        self.plugin = plugin

    def load(self):
        return self.plugin

@pytest.fixture(autouse=True)
def monkeypatch_maker_plugins(monkeypatch):
    from string import ascii_lowercase
    monkeypatch.setattr(freezerbox.model, 'MAKER_PLUGINS', {
        'sw': MockEntryPoint(StepwiseMaker),
        'order': MockEntryPoint(OrderMaker),
        'mock': MockEntryPoint(MockSoloMaker),
        'merge': MockEntryPoint(MockComboMaker),
        **{k: MockEntryPoint(MockSoloMaker) for k in ascii_lowercase},
    })

