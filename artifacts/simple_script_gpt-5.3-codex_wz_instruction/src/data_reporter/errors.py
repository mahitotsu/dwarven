"""Domain-specific exceptions with exit codes."""


class DataReporterError(Exception):
    """Base error for data-reporter."""

    exit_code: int = 1


class UserInputError(DataReporterError):
    """Raised when the input data or arguments are invalid."""

    exit_code = 2


class OutputError(DataReporterError):
    """Raised when the report cannot be written."""

    exit_code = 1
