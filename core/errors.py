
class ClientError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ServerError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class AdminExecuteError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
