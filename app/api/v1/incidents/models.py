from app.api.utils.base_model import Model

incident_list = [] 

class IncidentModel(Model):
    """Represents a model for storing incidents."""

    def __init__(self):
        """Initialize base model with data store reference."""

        super().__init__(incident_list)


