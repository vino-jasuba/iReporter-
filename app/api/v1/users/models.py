from app.api.v1.common.base_model import Model

user_list = []

class UserModel(Model):
    def __init__(self):
        super().__init__(user_list)
        self.guarded = ['password']