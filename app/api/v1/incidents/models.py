from app.api.utils.listmodel import ListModel

incident_list = [] 

class IncidentModel(ListModel):
    """Represents a model for storing incidents."""

    def __init__(self):
        """Initialize base model with data store reference."""

        super().__init__(incident_list)


