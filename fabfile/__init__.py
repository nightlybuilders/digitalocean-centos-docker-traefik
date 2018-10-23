from invoke import Collection

from . import bootstrap
from .stacks import infra


namespace = Collection(
    bootstrap,
    infra,
)