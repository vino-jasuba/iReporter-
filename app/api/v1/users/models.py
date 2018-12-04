from app.api.v1.common.base_model import Model

user_list = []

class UserModel(Model):
    """Represents a model for storing incidents."""

    def __init__(self):
        """Initialize base model with data store reference."""

        super().__init__(user_list)
