import unreal
import configparser
import sys
import os

# Добавление текущего пути в sys.path
sys.path.append(os.path.dirname(__file__))

from validators.StaticMeshValidator import StaticMeshValidator
from validators.SkeletalMeshValidator import SkeletalMeshValidator
from validators.TextureValidator import TextureValidator
from validators.MaterialValidator import MaterialValidator

# Загрузка конфигурационного файла
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'AssetValidationConfig.ini'))

# Проверка наличия секции 'Validators'
if not config.has_section('Validators'):
    raise ValueError("Конфигурационный файл не содержит секцию 'Validators'")

# Получение списка валидаторов из конфигурационного файла
validators = []
if config.getboolean('Validators', 'StaticMeshValidator'):
    unreal.log("Adding StaticMeshValidator")
    validators.append(StaticMeshValidator())
if config.getboolean('Validators', 'SkeletalMeshValidator'):
    unreal.log("Adding SkeletalMeshValidator")
    validators.append(SkeletalMeshValidator())
if config.getboolean('Validators', 'TextureValidator'):
    unreal.log("Adding TextureValidator")
    validators.append(TextureValidator())
if config.getboolean('Validators', 'MaterialValidator'):
    unreal.log("Adding MaterialValidator")
    validators.append(MaterialValidator())

# Метод для пометки ассета ошибкой
def mark_asset_error(asset, message):
    unreal.log_error(f"Asset: {asset.get_name()} - {message}")

# Получение выбранных ассетов
selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
unreal.log(f"Selected assets: {len(selected_assets)}")

# Валидация ассетов
for asset in selected_assets:
    unreal.log(f"Validating asset: {asset.get_name()}")
    for validator in validators:
        if validator.can_validate(asset):
            unreal.log(f"Using validator: {validator.__class__.__name__}")
            validator.validate(asset, mark_asset_error)