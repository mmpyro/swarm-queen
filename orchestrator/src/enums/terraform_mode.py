from enum import Enum


class TerraformMode(Enum):
    APPLY = 'apply'
    DESTROY = 'destroy'
