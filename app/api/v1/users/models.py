from app.api.utils.listmodel import ListModel

user_list = []

class UserModel(ListModel):
    """Represents a model for storing incidents."""

    def __init__(self):
        """Initialize base model with data store reference."""

        super().__init__(user_list)

    