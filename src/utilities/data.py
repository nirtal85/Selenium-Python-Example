from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass
class ForgotPassword:
    error_message: str
    success_message: str


@dataclass
class Login:
    error_message: str
    page_title: str


@dataclass
class Workspace:
    final_slide: str
    name: str
    new_name: str
    no_project_found_message: str
    non_existing_project: str
    page_title: str
    project_name: str
    project_type: str
    template_type: str


@dataclass_json
@dataclass
class Data:
    forgot_password: ForgotPassword
    login: Login
    workspace: Workspace
