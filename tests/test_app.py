from playwright.sync_api import expect

def test_get_index(page, test_web_address):
    page.goto(f"http://{test_web_address}/home")
    h2_tag = page.locator("h2#element-734ab6c")
    expect(h2_tag).to_contain_text("Welcome to Giga")

def test_get_about(page, test_web_address):
    page.goto(f"http://{test_web_address}/about")
    h2_tag = page.locator("h2#element-ad4752a")
    expect(h2_tag).to_contain_text("About Giga")

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
    h2_tag = page.locator("h2#element-632c964")
    expect(h2_tag).to_have_text("Gig: Portishead @ Brixton Academy")

def test_individual_band(page, test_web_address):
    page.goto(f"http://{test_web_address}/bands/Placebo")
    h2_tag = page.locator("h2#element-99ea37c")
    expect(h2_tag).to_have_text("Placebo: Gig Dates")
    gig_tags = page.locator("div.gig")
    expect(gig_tags).to_contain_text([
        "Placebo @ Brixton Academy, London\nWhen: 2025-12-01 19:30",
        "Placebo @ The Roundhouse, London\nWhen: 2025-12-08 20:00"
    ])

def test_get_login(page, test_web_address):
    page.goto(f"http://{test_web_address}/login")
    h2_tag = page.locator("h2#element-2b685e0")
    expect(h2_tag).to_contain_text("Log In")

def test_get_logout(page, test_web_address):
    page.goto(f"http://{test_web_address}/logout")
    h2_tag = page.locator("h2#element-064fcc0")
    expect(h2_tag).to_contain_text("Log Out")

def test_denied_access_to_account_page(web_client, test_web_address):
    response = web_client.get(f"http://{test_web_address}/account")
    assert response.status_code == 401

def test_can_switch_between_gigs_and_home(page, test_web_address):
    page.goto(f"http://{test_web_address}/home")
    page.click("text='Gigs'")
    h2_tag = page.locator("h2#element-c27b2f2")
    expect(h2_tag).to_contain_text("Gigs")
    page.click("text='Home'")
    h2_tag = page.locator("h2#element-734ab6c")
    expect(h2_tag).to_contain_text("Welcome to Giga")

def test_login_as_username(page, test_web_address, db_connection):
    db_connection.seed("seeds/test_users.sql")
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name='username']", "username")
    page.fill("input[name='password']", "password")
    page.click("text='Log in'")
    h2_tag = page.locator("h2")
    expect(h2_tag).to_have_text("Welcome to Giga, username")

def test_logout_as_username(logged_in_page_username, web_client, test_web_address):
    logged_in_page_username.goto(f"http://{test_web_address}/logout")
    logged_in_page_username.goto(f"http://{test_web_address}/account")
    h1_tag = logged_in_page_username.locator("h1")
    expect(h1_tag).to_have_text("401 Unauthorised")

def test_get_account_when_logged_in(logged_in_page_username, test_web_address, db_connection):
    db_connection.seed("seeds/test_bookings.sql")
    logged_in_page_username.goto(f"http://{test_web_address}/account")
    h2_tag = logged_in_page_username.locator("h2#element-1cfd0cf")
    expect(h2_tag).to_contain_text("Account")
    p_tags = logged_in_page_username.locator("p.element-35cbe6d")
    expect(p_tags).to_contain_text([
        "1 ticket for Placebo @ Brixton Academy, London on 2025-12-01 19:30",
        "4 tickets for Phantogram @ Corn Exchange, Cambridge on 2025-12-15 20:30"
    ])
