from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def get_value(cls, member):
        return cls[member].value[0]

    @classmethod
    def get_choices(cls):
        return tuple(x.value for x in cls)


class IncidentType(ChoiceEnum):
    individual = ('I', 'Individual')
    enterprise = ('E', 'Enterprise')
    government = ('G', 'Government')


class UserType(ChoiceEnum):
    customer = ('C', 'Customer')
    rider = ('R', 'Rider')
    restaurant = ('rt', 'Restaurant')


class PriorityType(ChoiceEnum):
    high = ('H', 'High')
    medium = ('M', 'Medium')
    low = ('L', 'Low')


class StatusType(ChoiceEnum):
    in_progress = ('0', 'In Progress')
    accepted = ('1', 'Accepted')
    rejected = ('2', 'Rejected')
    picked = ('3', 'Picked')
    delivered = ('4', 'Delivered')
