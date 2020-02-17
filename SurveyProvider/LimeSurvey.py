from flask import current_app as app

from model.Survey import Survey


class LimeSurvey:
    """
    A class that retrieves survey data from a Survey Gizmo survey
    """

    @property
    def survey(self):
        """
        the survey object as obtained from Survey Gizmo
        :return: the survey object
        """
        return self._survey

    def __init__(self, survey_id, project_id):
        # get the credentials from the config
        with app.app_context():
            self._key = app.config.get("LIME_SURVEY_URL")
            self._secret = app.config.get("LIME_SURVEY_KEY")
        self._survey = Survey(survey_id=survey_id, project_id=project_id)
