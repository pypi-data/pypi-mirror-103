from daipecore.lineage.argument.DecoratorInputFunctionInterface import DecoratorInputFunctionInterface


class FileRead(DecoratorInputFunctionInterface):
    def __init__(self, path: str):
        self.__path = path

    @property
    def path(self):
        return self.__path
