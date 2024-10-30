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


class Categories(enum.Enum):
    TECHNOLOGY = "TECHNOLOGY"
    LIFE_STYLE = "LIFE"
    SELF_DEVELOPMENT = "SELF DEVELOPMENT"
    AI = "AI"
    NEWS = "NEWS"
    PROGRESS = "PROGRESS"

class VoteType(enum.Enum):
    UPVOTE = 1
    DOWNVOTE = -1
