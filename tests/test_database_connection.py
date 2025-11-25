from lib.database_connection import DatabaseConnection
import pytest

def test_database_name_method_uses_constants():
    dbc = DatabaseConnection(True)
    assert dbc._database_name() == dbc.TEST_DATABASE_NAME
    dbc.test_mode = False
    assert dbc._database_name() == dbc.DEV_DATABASE_NAME

def test_exception_when_database_not_created():
    dbc = DatabaseConnection(True)
    dbc.TEST_DATABASE_NAME = "thiswasnotcreated"
    with pytest.raises(Exception) as e:
        dbc.connect()
    assert str(e.value) == "Couldn't connect to the database thiswasnotcreated! Did you create it using `createdb thiswasnotcreated`?"

def test_exception_when_no_connection():
    dbc = DatabaseConnection(True)
    with pytest.raises(Exception) as e:
        dbc._check_connection()
    assert "Cannot run a SQL query" in str(e.value)

def test_exception_when_unknown_seed_file():
    dbc = DatabaseConnection(True)
    dbc.connect()
    with pytest.raises(Exception) as e:
        dbc.seed("doesnotexist.sql")
    assert str(e.value) == "File doesnotexist.sql does not exist"
