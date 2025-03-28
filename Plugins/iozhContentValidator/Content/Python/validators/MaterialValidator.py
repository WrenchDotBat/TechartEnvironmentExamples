import unreal
import configparser
import os

class MaterialValidator:
    def __init__(self):
        # Загрузка конфигурационного файла
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), '..', 'AssetValidationConfig.ini'))
        
        # Загрузка параметров из конфигурационного файла
        self.max_texture_size = config.getint('MaterialValidator', 'MaxTextureSize')

    def can_validate(self, asset):
        return isinstance(asset, unreal.Material)

    def validate(self, asset, mark_asset_error):
        unreal.log(f"Validating Material: {asset.get_name()}")