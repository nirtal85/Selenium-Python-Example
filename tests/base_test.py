from abc import ABC
from typing import Union

from selenium.webdriver import Chrome, Edge, Firefox
from selenium.webdriver.support.wait import WebDriverWait

from pages.about_page import AboutPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.login_page import LoginPage
from pages.project_edit_page import ProjectEditPage
from pages.project_type_page import ProjectTypePage
from pages.projects_page import ProjectsPage
from pages.templates_page import TemplatesPage
from utilities.mailinator_helper import MailinatorHelper
from utilities.vrt_helper import VrtHelper


class BaseTest(ABC):
    driver: Union[Chrome, Firefox, Edge]
    wait: WebDriverWait
    about_page: AboutPage
    login_page: LoginPage
    projects_page: ProjectsPage
    forget_password_page: ForgotPasswordPage
    templates_page: TemplatesPage
    project_type_page: ProjectTypePage
    project_edit_page: ProjectEditPage
    vrt_helper: VrtHelper
    mailinator_helper: MailinatorHelper
