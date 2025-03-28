import unreal
import configparser
import os

class TextureValidator:
    def __init__(self):
        # Загрузка конфигурационного файла
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), '..', 'AssetValidationConfig.ini'))
        
        # Загрузка параметров из конфигурационного файла
        self.max_resolution = config.getint('TextureValidator', 'MaxResolution')

    def can_validate(self, asset):
        return isinstance(asset, unreal.Texture)

    def validate(self, asset, mark_asset_error):
        # Загрузка ассета для полной доступности данных
        loaded_asset = unreal.EditorAssetLibrary.load_asset(asset.get_path_name())
        unreal.log(f"Validating Texture: {loaded_asset.get_name()}")
        self.check_resolution(loaded_asset, mark_asset_error)
        self.check_power_of_two(loaded_asset, mark_asset_error)

    def check_resolution(self, asset, mark_asset_error):
        width = asset.blueprint_get_size_x()
        height = asset.blueprint_get_size_y()
        unreal.log(f"Checking resolution: Asset has resolution {width}x{height}.")
        if width > self.max_resolution or height > self.max_resolution:
            mark_asset_error(asset, f"has resolution {width}x{height}, which exceeds the limit of {self.max_resolution}.")

    def check_power_of_two(self, asset, mark_asset_error):
        width = asset.blueprint_get_size_x()
        height = asset.blueprint_get_size_y()
        unreal.log(f"Checking power of two: Asset has dimensions {width}x{height}.")
        if not (self.is_power_of_two(width) and self.is_power_of_two(height)):
            mark_asset_error(asset, f"has dimensions {width}x{height}, which are not power of 2.")

    def is_power_of_two(self, n):
        return (n & (n - 1) == 0) and n != 0