import allure

from pages.top_bars.top_navigate_bar import TopNavigateBar


class ProjectsPage(TopNavigateBar):
    """ Projects page - Where projects are added and edited"""

    def __init__(self):
        super().__init__()
        self._start_btn = "#app .px-4 a"
        self._create_new_workspace_btn = ".font-medium button"
        self._workspace_edit_btn = "[data-icon='chevron-down']"
        self._rename_workspace_btn = ".mr-3 .hover\\:bg-gray-600"
        self._delete_workspace_btn = ".mr-3 .text-red-600"
        self._rename_field = ".vue-portal-target input"
        self._confirmation_btn = "#confirm-create-button"
        self._new_workspace_name_field = "[placeholder='Workspace name']"
        self._delete_workspace_field = ".h-12"
        self._create_project_btn = ".hidden.px-3"
        self._search_btn = "[data-icon='search']"
        self._search_field = "[type='text']"
        self._confirm_delete_project_btn = "#confirm-delete-button"
        self._cancel_project_deletion_btn = "form [type='button'"
        self._project_page_title = "#app h1.leading-tight.truncate"

    @allure.step("Get projects' page title")
    def get_title(self):
        el = self._driver.find_element_by_css_selector(self._project_page_title)
        return self.get_text(el)
