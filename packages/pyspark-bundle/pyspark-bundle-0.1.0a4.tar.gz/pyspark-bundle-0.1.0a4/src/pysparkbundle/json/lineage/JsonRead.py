from pysparkbundle.lineage.FileRead import FileRead


class JsonRead(FileRead):
    @property
    def type(self):
        return "json"
