#!/usr/bin/env python

"""Tests for `geochron` subpackage."""

import pytest
from geo_calcs.calculations.geochron import *

def test_calc_t2_daughter():
    assert calc_t2_daughter(16, 0.1, 1.55125*10**-10, 2000) == 16.03637660130213 # Check this later





