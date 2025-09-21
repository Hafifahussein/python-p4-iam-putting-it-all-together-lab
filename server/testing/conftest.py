#!/usr/bin/env python3

import pytest
from app import app, db
from models import User, Recipe

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))

@pytest.fixture(scope='function', autouse=True)
def setup_database():
    """Set up the database before each test and tear down after"""
    with app.app_context():
        # Create all tables
        db.create_all()
        yield
        # Clean up after test
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client():
    """Test client fixture"""
    with app.test_client() as client:
        with app.app_context():
            yield client