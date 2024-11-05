
class CommentNotFound(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail


class PermissionDenied(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail