class VariableFormatError(ValueError):
    "Raised when clip is of a variable format."
    def __init__(self, function: str, message: str = "{func}: 'Variable-format clips not supported!'") -> None:
        self.function: str = function
        self.message: str = message
        super().__init__(self.message.format(func=self.function))


class VariableResolutionError(ValueError):
    "Raised when clip is of a variable resolution."
    def __init__(self, function: str, message: str = "{func}: 'Variable-resolution clips not supported!'") -> None:
        self.function: str = function
        self.message: str = message
        super().__init__(self.message.format(func=self.function))
