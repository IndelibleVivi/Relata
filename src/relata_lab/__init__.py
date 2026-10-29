"""Relata's offline, local research workspace."""
from .core import Lab, LabError
from . import compat

__all__ = ["Lab", "LabError", "compat"]
