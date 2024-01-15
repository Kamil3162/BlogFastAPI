import enum
class BlacklistReason(enum.Enum):
    SPAM = "Spamming or irrelevant messages"
    ABUSE = "Abusive behavior"
    HACK_ATTEMPT = "Attempted security breach"
    OTHER = "Other"


class UserRoles(enum.Enum):
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
    BLOGGER = "BLOGGER"
    ANONYMOUS_USER = "ANONYMOUS_USER"