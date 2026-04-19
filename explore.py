from playwright.sync_api import sync_playwright
from config import  Base_URL
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://eg.hatla2ee.com/ar/car")
    page_num=5
    #=input("Enter the page number: ")
    page.goto(f'{Base_URL}/ar/car/{page_num}')

    # Extract all the links with the class "no-underline"
    links = page.locator("a.no-underline").evaluate_all(
        "elements => elements.map(el => el.getAttribute('href'))"
    )

    #validate the links
    #valid_links = [link for link in links if link and link.startswith("/ar/new-car/")]
    valid_links = list(dict.fromkeys([
        l for l in links if l and "/showroom/" not in l
    ]))

    page.goto(f"{Base_URL}{valid_links[1]}")
    #print div list with class "overview"
    overview = page.locator("#listing-overview")
    #print title of div with class "listing-overview"
    title = overview.locator("h1").inner_text().strip()
    #print all span with class "font-medium" in div with class "listing-overview"
    info=overview.locator("span.font-medium").all_inner_texts()
    years=overview.locator("span.font-medium").nth(0).inner_text().strip()
    km=info[1].strip()
    transmission=info[2].strip()
    fuel=info[3].strip()

    #print price of div with class "listing-overview"
    price = overview.locator(".text-2xl.text-primary-800").inner_text()
    price=int(price.replace("جنيه","").replace(",","").strip())
    
    #description 
    descreption=page.locator("#description").inner_text().strip()
    #details 
    details=page.locator("#car-details")
    data = {}

    for item in details.all():
        cols = item.locator("div")

        if cols.count() == 2:
            key = cols.nth(0).inner_text().strip()
            value = cols.nth(1).inner_text().strip()

            data[key] = value
    
    
    features = {}

    feature_container = page.locator("h2#features + div")
    sections = feature_container.locator(".grid > div > .flex.flex-col.gap-2")

    for section in sections.all():
        section_title = section.locator("span.font-bold").first.inner_text().strip()
        items = section.locator("span.text-sm:not(.font-bold)").all_inner_texts()
        features[section_title] = [item.strip() for item in items]     



    print(f"Title: {title}\nYear: {years}\nKM: {km}\nTransmission: {transmission}\nFuel: {fuel}")
    print(f"Price: {price}")
    print(f"Description: {descreption}")
    print("Details:")
    print(data)
    print("Features:")  
    for section, items in features.items():
        print(f"{section}:")
        for item in items:
            print(f" - {item}")
    #print(title)

    #print(valid_links)
    #print(links)

    page.screenshot(path="google.png")
    page.wait_for_timeout(5000)
    browser.close()