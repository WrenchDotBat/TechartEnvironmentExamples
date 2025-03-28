import unreal

# Define the prefix you want to add
PREFIX = "MyPrefix_"

# Get the selected assets
selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()

# Iterate over each selected asset and rename it with the prefix
for asset in selected_assets:
    asset_name = asset.get_name()
    new_name = PREFIX + asset_name
    asset_path = asset.get_path_name()
    new_path = asset_path.replace(asset_name, new_name)
    unreal.EditorAssetLibrary.rename_asset(asset_path, new_path)
    print(f"Renamed {asset_name} to {new_name}")
