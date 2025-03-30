import unreal

def say_hi():
    unreal.log("HI!")
    
def read_selected_textures():
    EditorAssetLibrary = unreal.EditorAssetLibrary()
    assets_list = unreal.EditorUtilityLibrary().get_selected_assets()
    for asset in assets_list:
        texture = EditorAssetLibrary.load_asset(asset.get_path_name())
        
        asset_tag = EditorAssetLibrary.get_metadata_tag(asset, "AssetType")
        unreal.log(asset_tag)
        
        
        #if isinstance(asset, unreal.Texture2D):
         #   unreal.log(f"Processing texture: {asset.get_name()}, AssetType: {asset_type}")
          #  # Здесь можно добавить код для работы с текстурой
        #else:
        #    unreal.log("Not a texture: " + asset.get_name())
        
def get_metadata_tag():
    EditorAssetLibrary = unreal.EditorAssetLibrary()
    assets_list = unreal.EditorUtilityLibrary().get_selected_assets()
    for asset in assets_list:
        asset_tag = EditorAssetLibrary.get_metadata_tag(asset, "AssetType")
        unreal.log(asset_tag)
        

def set_metadata_tag():
    EditorAssetLibrary = unreal.EditorAssetLibrary()
    assets_list = unreal.EditorUtilityLibrary().get_selected_assets()
    for asset in assets_list:
        EditorAssetLibrary.set_metadata_tag(asset, "AssetType", "TestGroup")
        EditorAssetLibrary.save_asset(asset)