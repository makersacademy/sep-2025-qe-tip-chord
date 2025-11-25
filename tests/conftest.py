import pytest, sys, random, py, os
from xprocess import ProcessStarter
from lib.database_connection import DatabaseConnection
from app import app
from playwright.sync_api import sync_playwright

@pytest.fixture
def page():
    def make_page(playwright):
        browser = playwright.chromium.launch()
        page = browser.new_context().new_page()
        return page
    with sync_playwright() as playwright:
        yield make_page(playwright)

@pytest.fixture
def db_connection():
    conn = DatabaseConnection(test_mode=True)
    conn.connect()
    return conn

@pytest.fixture
def test_web_address(xprocess):
    python_executable = sys.executable
    app_file = py.path.local(__file__).dirpath("../app.py")
    port = str(random.randint(4100, 4199))
    class Starter(ProcessStarter):
        env = {"PORT": port, "APP_ENV": "test", **os.environ}
        pattern = "Debugger PIN"
        args = [python_executable, app_file]

    xprocess.ensure("flask_test_server", Starter)

    yield f"localhost:{port}"

    xprocess.getinfo("flask_test_server").terminate()

@pytest.fixture
def web_client():
    app.config['TESTING'] = True # This gets us better errors
    with app.test_client() as client:
        yield client

@pytest.fixture
def logged_in_page_username(page, test_web_address, db_connection):
    db_connection.seed("seeds/test_users.sql")
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name='username']", "username")
    page.fill("input[name='password']", "password")
    page.click("text='Log in'")
    return page
