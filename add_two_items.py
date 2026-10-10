from playwright.sync_api import sync_playwright, expect


def add_cheapest_and_priciest(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        page.goto(url)

        page.get_by_role("textbox", name="Username").fill("standard_user")
        page.get_by_role("textbox", name="Password").fill("secret_sauce")
        page.get_by_role("button", name="Login").click()
        page.wait_for_url("**/inventory.html")

        items = page.locator("[data-test='inventory-item']")

        products = []
        for i in range(items.count()):
            item = items.nth(i)
            name = item.locator("[data-test='inventory-item-name']").inner_text()
            price = float(item.locator("[data-test='inventory-item-price']").inner_text().replace("$", ""))
            products.append((name, price, item))

        cheapest = min(products, key=lambda x: x[1])
        priciest = max(products, key=lambda x: x[1])

        for name, price, item in (cheapest, priciest):
            item.get_by_role("button", name="Add to cart").click()
            print(f"Додано: {name} (${price})")

        expect(page.locator("[data-test='shopping-cart-badge']")).to_have_text("2")
        page.locator("[data-test='shopping-cart-link']").click()
        page.wait_for_url("**/cart.html")


        cart_names = page.locator("[data-test='inventory-item-name']").all_inner_texts()
        assert set(cart_names) == {cheapest[0], priciest[0]}


        browser.close()

if __name__ == "__main__":
    add_cheapest_and_priciest("https://www.saucedemo.com/")