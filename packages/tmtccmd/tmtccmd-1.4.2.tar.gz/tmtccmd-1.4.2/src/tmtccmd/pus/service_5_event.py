import enum


class Srv5Subservices(enum.IntEnum):
    INFO_EVENT = 1,
    LOW_SEVERITY_EVENT = 2,
    MEDIUM_SEVERITY_EVENT = 3,
    HIGH_SEVERITY_EVENT = 4,
    ENABLE_EVENT_REPORTING = 5,
    DISABLE_EVENT_REPORTING = 6
