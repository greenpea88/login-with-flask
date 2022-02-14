from login.repositories import BaseUserRepo


class MemUserRepo(BaseUserRepo):
    def get(self, user_id):
        pass

    def get_by_username(self, username):
        pass

    def list(self):
        pass


class DBUserRepo(BaseUserRepo):
    def get(self, user_id):
        pass

    def get_by_username(self, username):
        pass

    def list(self):
        pass
