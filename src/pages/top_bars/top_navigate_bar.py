import allure
from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage


class TopNavigateBar(BasePage):
    """Top navigation bar - the bar that appears at the top of the page after login"""

    PROJECTS_BTN = (By.CSS_SELECTOR, "[href='https://app.involve.me/projects']")
    TEMPLATES_BTN = (By.CSS_SELECTOR, "[href='https://app.involve.me/templates']")
    ANALYTICS_BTN = (By.CSS_SELECTOR, "[href='https://app.involve.me/analytics']")
    INTEGRATIONS_BTN = (By.CSS_SELECTOR, "[href='https://app.involve.me/integrations']")
    AFFILIATE_PROGRAM_BTN = (
        By.CSS_SELECTOR,
        "[href='https://app.involve.me/affiliate']",
    )
    ACCOUNT_DROP_DOWN_MENU = (By.CSS_SELECTOR, "#nav-dropdown")
    LOGOUT_BTN = (By.CSS_SELECTOR, "[href='https://app.involve.me/logout']")

    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    @allure.step("Click Projects tab")
    def click_projects(self):
        self.click(self.PROJECTS_BTN)

    @allure.step("Click Templates tab")
    def click_templates(self):
        self.click(self.TEMPLATES_BTN)

    @allure.step("Click Analytics tab")
    def click_analytics(self):
        self.click(self.ANALYTICS_BTN)

    @allure.step("Click Integrations tab")
    def click_integrations(self):
        self.click(self.INTEGRATIONS_BTN)

    @allure.step("Click Affiliate Program tab")
    def click_affiliate_program(self):
        self.click(self.AFFILIATE_PROGRAM_BTN)

    @allure.step("Logout from system")
    def logout(self):
        # Click account drop down menu
        self.click(self.ACCOUNT_DROP_DOWN_MENU)
        # Click logout button
        self.click(self.LOGOUT_BTN)
