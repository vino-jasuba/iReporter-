from app.api.v1.common.base_model import Model


class UserModel(Model):
    def __init__(self, user_list):
        super().__init__(user_list)