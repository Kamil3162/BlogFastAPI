import enum
class BlacklistReason(enum.Enum):
    SPAM = "Spamming or irrelevant messages"
    ABUSE = "Abusive behavior"
    HACK_ATTEMPT = "Attempted security breach"
    OTHER = "Other"
