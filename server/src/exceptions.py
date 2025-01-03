
class ClientException(Exception):
    """ 클라이언트 예외 """
    message: str

    def __init__(self, message: str, **kwargs):
        self.message = message
        super().__init__(**kwargs)

class ServerException(Exception):
    """ 서버 예외 """
    message: str

    def __init__(self, message: str, **kwargs):
        self.message = message
        super().__init__(**kwargs)

