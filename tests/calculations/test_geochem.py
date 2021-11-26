#!/usr/bin/env python

"""Tests for `geochem` subpackage."""

import pytest
from geo_calcs.calculations.geochem import *

def test_get_atomic_weight():
    assert get_atomic_weight(["Si","O","O"]) == 60.0843 
    