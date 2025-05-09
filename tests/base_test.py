from abc import ABC

from selenium.webdriver import Chrome, Edge, Firefox
from selenium.webdriver.support.wait import WebDriverWait

from src.pages.about_page import AboutPage
from src.pages.forgot_password_page import ForgotPasswordPage
from src.pages.login_page import LoginPage
from src.pages.project_edit_page import ProjectEditPage
from src.pages.project_type_page import ProjectTypePage
from src.pages.projects_page import ProjectsPage
from src.pages.templates_page import TemplatesPage
from src.utilities.mailinator_helper import MailinatorHelper
from src.utilities.vrt_helper import VrtHelper


class BaseTest(ABC):
    driver: Chrome | Firefox | Edge
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
