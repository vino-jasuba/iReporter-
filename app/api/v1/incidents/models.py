from app.api.v1.common.base_model import Model


class IncidentModel(Model):

    def __init__(self, incident_list):
        super().__init__(incident_list)


