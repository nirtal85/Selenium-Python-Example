from pages.basepage import BasePage


class ProjectsPage(BasePage):
    """ Projects page - Where projects are added and edited"""

    def __init__(self):
        super().__init__()
        self.start_btn = ""
        self.create_new_workspace_btn = ""
        self.workspace_edit_btn = ""
        self.rename_workspace_btn = ""
        self.delete_workspace_btn = ""
        self.rename_field = ""
        self.confirmation_btn = ""
        self.new_workspace_name_field = ""
        self.delete_workspace_field = ""
        self.create_project_btn = ""
        self.search_btn = ""
        self.search_field = ""
        self.confirm_delete_project_btn = ""
        self.cancel_project_deletion_btn = ""