"""Domain errors kept separate from command-line presentation."""


class TaskError(Exception):
    """Base class for expected invalid task operations."""


class ValidationError(TaskError):
    """Raised when an input field cannot be accepted."""


class StorageError(TaskError):
    """Raised when task data cannot be read or written."""


class MissingTask(TaskError):
    """Raised when an operation names an absent task."""


class MissingProject(TaskError):
    """Raised when a task refers to an absent project."""
