import unreal
import configparser
import os

class SkeletalMeshValidator:
    def __init__(self):
        # Загрузка конфигурационного файла
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), '..', 'AssetValidationConfig.ini'))
        
        # Загрузка параметров из конфигурационного файла
        self.max_bones = config.getint('SkeletalMeshValidator', 'MaxBones')
        self.max_polygons = config.getint('SkeletalMeshValidator', 'MaxPolygons')

    def can_validate(self, asset):
        return isinstance(asset, unreal.SkeletalMesh)

    def validate(self, asset, mark_asset_error):
        unreal.log(f"Validating SkeletalMesh: {asset.get_name()}")