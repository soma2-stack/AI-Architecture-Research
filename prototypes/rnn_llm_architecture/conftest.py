"""Limit this architecture test suite to a single CPU thread."""
import torch
import pytest


def pytest_sessionstart(session):
    torch.set_num_threads(1)


@pytest.fixture(autouse=True)
def reproducible_cpu_test_inputs():
    torch.manual_seed(20261007)
