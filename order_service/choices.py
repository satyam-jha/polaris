from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def get_value(cls, member):
        return cls[member].value[0]

    @classmethod
    def get_choices(cls):
        return tuple(x.value for x in cls)


class UserType(ChoiceEnum):
    customer = ('C', 'Customer')
    rider = ('R', 'Rider')
    restaurant = ('rt', 'Restaurant')


class StatusType(ChoiceEnum):
    open = ('O', 'Open')
    closed = ('C', 'Closed')
    in_progress = ('P', 'In Progress')
