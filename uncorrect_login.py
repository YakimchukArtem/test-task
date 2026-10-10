from playwright.sync_api import sync_playwright, expect

result_file = open("Result_test.txt", "a", encoding="utf-8")


def uncorrect_login(url):
  with sync_playwright() as p:
    print("###########   2   ###########", file=result_file)
    browser = p.chromium.launch(headless=False, slow_mo=1000)
    page = browser.new_page()
    page.goto(url)
    print("Відкрито успішно сторінку!", file=result_file)
    page.get_by_role("textbox", name="Username").fill("locked_out_user")
    page.get_by_role("textbox", name="Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    print("Спроба виконати вхід в систему", file=result_file)
    error = page.locator("[data-test='error']")
    print("Помилка входу", file=result_file)
    expect(error).to_be_visible()
    expect(error).to_contain_text("Sorry, this user has been locked out")
    print("Sorry, this user has been locked out", file=result_file)
    expect(page).to_have_url(url)

    browser.close()


if __name__ == "__main__":
  uncorrect_login(url = "https://www.saucedemo.com/")