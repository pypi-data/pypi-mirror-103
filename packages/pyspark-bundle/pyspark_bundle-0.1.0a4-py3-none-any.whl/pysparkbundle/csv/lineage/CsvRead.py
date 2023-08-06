from pysparkbundle.lineage.FileRead import FileRead


class CsvRead(FileRead):
    @property
    def type(self):
        return "csv"
