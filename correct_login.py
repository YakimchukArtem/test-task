from playwright.sync_api import sync_playwright

result_file = open("Result_test.txt", "a", encoding="utf-8")


def correct_login(url):
  with sync_playwright() as p:
    print("###########   1   ###########", file=result_file)
    browser = p.chromium.launch(headless=False, slow_mo=1000)
    page = browser.new_page()
    page.goto(url)
    print("Відкрито успішно сторінку!", file=result_file)
    page.get_by_role("textbox", name="Username").fill("standard_user")
    page.get_by_role("textbox", name="Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    print("Спроба виконати вхід в систему", file=result_file)
    page.get_by_role("button", name="Open Menu").click()
    print("Знайдено меню вибору", file=result_file)
    page.get_by_role("button", name="Logout").click()
    print("Виконано Logout", file=result_file)   
    browser.close()
    print("Успішно виконаний тест!", file=result_file)



if __name__ == "__main__":
  correct_login(url = "https://www.saucedemo.com/")