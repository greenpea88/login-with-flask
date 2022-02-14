import abc


class BaseUserRepo(abc.ABC):

    @abc.abstractmethod
    def get(self, user_id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_username(self, username):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self):
        raise NotImplementedError
