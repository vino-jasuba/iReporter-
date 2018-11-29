from app.api.v1.common.base_model import Model

incident_list = [] 

class IncidentModel(Model):

    def __init__(self):
        super().__init__(incident_list)


