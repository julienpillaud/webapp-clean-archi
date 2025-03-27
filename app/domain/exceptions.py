class DomainError(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class NotFoundError(DomainError):
    pass


class AlreadyExistsError(DomainError):
    pass
