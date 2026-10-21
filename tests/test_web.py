import os

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


HUB_URL = os.getenv(
    "SELENIUM_HUB_URL",
    "http://localhost:4444"
)


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    browser = webdriver.Remote(
        command_executor=HUB_URL,
        options=options
    )
    browser.set_page_load_timeout(30)
    yield browser
    browser.quit()


class TestExampleDomain:
    def test_page_title(self, driver):
        driver.get("https://example.com")
        assert driver.title == "Example Domain"

    def test_page_heading(self, driver):
        driver.get("https://www.selenium.dev/selenium/web/web-form.html")

        heading = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.TAG_NAME, "h1"))
        )

        assert heading.text == "Web form"


class TestDuckDuckGo:
    def test_search_input(self, driver):
        driver.get("https://duckduckgo.com/")
        search = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.NAME, "q"))
        )
        search.send_keys("Selenium Python")
        assert search.get_attribute("value") == "Selenium Python"

    def test_search_submission(self, driver):
        driver.get("https://duckduckgo.com/")
        search = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.NAME, "q"))
        )
        search.send_keys("Selenium Python")
        search.send_keys(Keys.ENTER)

        WebDriverWait(driver, 20).until(
            lambda browser: "Selenium Python" in browser.title
        )
        assert "Selenium Python" in driver.title
