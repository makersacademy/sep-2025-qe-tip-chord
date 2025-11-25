from playwright.sync_api import expect

def test_get_index(page, test_web_address):
    page.goto(f"http://{test_web_address}/home")
    p_tag = page.locator("p#element-734ab6c")
    expect(p_tag).to_contain_text("Welcome to Giga")

def test_get_about(page, test_web_address):
    page.goto(f"http://{test_web_address}/about")
    p_tag = page.locator("p#element-ad4752a")
    expect(p_tag).to_contain_text("About Giga")

def test_gigs(page, test_web_address, db_connection):
    db_connection.seed("seeds/test_gigs.sql")
    page.goto(f"http://{test_web_address}/gigs")
    gig_tags = page.locator("div")
    expect(gig_tags).to_contain_text([
        "Placebo @ Brixton Academy, London\n2025-12-01 19:30",
        "Portishead @ Brixton Academy, London\n2025-12-08 19:30",
        "Placebo @ The Roundhouse, London\n2025-12-08 20:00",
        "Phantogram @ Corn Exchange, Cambridge\n2025-12-15 20:30"
    ])

def test_individual_gig(page, test_web_address):
    page.goto(f"http://{test_web_address}/gigs/2")
    p_tag = page.locator("p#element-632c964")
    expect(p_tag).to_have_text("Gig: Portishead @ Brixton Academy")

def test_get_login(page, test_web_address):
    page.goto(f"http://{test_web_address}/login")
    p_tag = page.locator("p#element-2b685e0")
    expect(p_tag).to_contain_text("Log In")

def test_get_logout(page, test_web_address):
    page.goto(f"http://{test_web_address}/logout")
    p_tag = page.locator("p#element-064fcc0")
    expect(p_tag).to_contain_text("Log Out")

def test_can_switch_between_gigs_and_home(page, test_web_address):
    page.goto(f"http://{test_web_address}/home")
    page.click("text='Gigs'")
    p_tag = page.locator("p#element-c27b2f2")
    expect(p_tag).to_contain_text("Gigs")
    page.click("text='Home'")
    p_tag = page.locator("p#element-734ab6c")
    expect(p_tag).to_contain_text("Welcome to Giga")
