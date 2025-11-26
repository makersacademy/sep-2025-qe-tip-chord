from playwright.sync_api import expect

def test_get_index(page, test_web_address):
    page.goto(f"http://{test_web_address}/")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_contain_text("Welcome to Giga")

def test_get_home(page, test_web_address):
    page.goto(f"http://{test_web_address}/home")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_contain_text("Welcome to Giga")

def test_get_about(page, test_web_address):
    page.goto(f"http://{test_web_address}/about")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_contain_text("About Giga")

def test_gigs(page, test_web_address, db_connection):
    db_connection.seed("seeds/test_gigs.sql")
    page.goto(f"http://{test_web_address}/gigs")
    gig_tags = page.locator("div.gig")
    expect(gig_tags).to_contain_text([
        "Placebo @ Brixton Academy, London\nWhen: 2025-12-01 19:30",
        "Portishead @ Brixton Academy, London\nWhen: 2025-12-08 19:30",
        "Placebo @ The Roundhouse, London\nWhen: 2025-12-08 20:00",
        "Phantogram @ Corn Exchange, Cambridge\nWhen: 2025-12-15 20:30"
    ])

def test_individual_gig(page, test_web_address):
    page.goto(f"http://{test_web_address}/gigs/2")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Gig: Portishead @ Brixton Academy")

def test_individual_band(page, test_web_address):
    page.goto(f"http://{test_web_address}/bands/Placebo")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Placebo: Gig Dates")
    gig_tags = page.locator("div.gig")
    expect(gig_tags).to_contain_text([
        "Placebo @ Brixton Academy, London\nWhen: 2025-12-01 19:30",
        "Placebo @ The Roundhouse, London\nWhen: 2025-12-08 20:00"
    ])

def test_get_login(page, test_web_address):
    page.goto(f"http://{test_web_address}/login")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_contain_text("Log In")

def test_get_signup(page, test_web_address):
    page.goto(f"http://{test_web_address}/signup")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_contain_text("Sign Up")

def test_get_logout(page, test_web_address):
    page.goto(f"http://{test_web_address}/logout")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_contain_text("Log Out")

def test_denied_access_to_account_page(web_client, test_web_address):
    response = web_client.get(f"http://{test_web_address}/account")
    assert response.status_code == 401

def test_can_switch_between_gigs_and_home(page, test_web_address):
    page.goto(f"http://{test_web_address}/home")
    page.click("text='Gigs'")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_contain_text("Gigs")
    page.click("text='Home'")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_contain_text("Welcome to Giga")

def test_login_as_username(page, test_web_address, db_connection):
    db_connection.seed("seeds/test_users.sql")
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name='username']", "username")
    page.fill("input[name='password']", "password")
    page.click("text='Log in'")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Welcome to Giga, username")

def test_logout_as_username(logged_in_page_username, web_client, test_web_address):
    logged_in_page_username.goto(f"http://{test_web_address}/logout")
    logged_in_page_username.goto(f"http://{test_web_address}/account")
    h2_tag = logged_in_page_username.locator("h2")
    expect(h2_tag).to_have_text("401 Unauthorised")

def test_get_account_when_logged_in(logged_in_page_username, test_web_address, db_connection):
    db_connection.seed("seeds/test_bookings.sql")
    logged_in_page_username.goto(f"http://{test_web_address}/account")
    h1_tag = logged_in_page_username.locator("h1")
    expect(h1_tag).to_contain_text("Account")
    p_tags = logged_in_page_username.locator("p.booking-text")
    expect(p_tags).to_contain_text([
        "1 ticket for Placebo @ Brixton Academy, London on 2025-12-01 19:30",
        "4 tickets for Phantogram @ Corn Exchange, Cambridge on 2025-12-15 20:30"
    ])

def test_book_gig(logged_in_page_username, test_web_address, db_connection):
    db_connection.seed("seeds/test_bookings.sql")
    logged_in_page_username.goto(f"http://{test_web_address}/gigs/2")
    logged_in_page_username.fill("input[name='ticket_count']", "7")
    logged_in_page_username.click("text='Book gig'")
    p_tags = logged_in_page_username.locator("p.booking-text")
    expect(p_tags).to_contain_text([
        "1 ticket for Placebo @ Brixton Academy, London on 2025-12-01 19:30",
        "4 tickets for Phantogram @ Corn Exchange, Cambridge on 2025-12-15 20:30",
        "7 tickets for Portishead @ Brixton Academy, London on 2025-12-08 19:30"
    ])
