class ProjectList:

    @property
    def projects(self):
        return self._projects

    def __init__(self, projects=None):
        if projects is not None:
            self._projects = projects
        else:
            self._projects = []

    def add_project(self, project):
        self._projects.append(project)

    def __getstate__(self):
        state = self.__dict__.copy()
        return {k.lstrip('_'): v for k, v in state.items()}