from daipecore.lineage.argument.ArgumentMappingInterface import ArgumentMappingInterface
from pysparkbundle.csv.lineage.CsvRead import CsvRead
from pysparkbundle.json.lineage.JsonRead import JsonRead


class ArgumentMapping(ArgumentMappingInterface):
    def get_mapping(self):
        return {
            "read_csv": CsvRead,
            "read_json": JsonRead,
        }
