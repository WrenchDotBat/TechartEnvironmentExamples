import unreal
import time

def say_hi():
    unreal.log("HI!")
    
def print_texture_compressions():
    EditorAssetLibrary = unreal.EditorAssetLibrary()
    assets_list = unreal.EditorUtilityLibrary().get_selected_assets()
    for asset in assets_list:
        texture = EditorAssetLibrary.load_asset(asset.get_path_name())
        
        if isinstance(texture, unreal.Texture2D):
            unreal.log(f"Processing texture: {asset.get_name()}, Compression: {texture.get_editor_property('compression_settings')}")
        else:
            unreal.log("Not a texture: " + asset.get_name())
            
def fix_normalmap_compression():
    EditorAssetLibrary = unreal.EditorAssetLibrary()
    assets_list = unreal.EditorUtilityLibrary().get_selected_assets()
    for asset in assets_list:
        texture = EditorAssetLibrary.load_asset(asset.get_path_name())
        
        if isinstance(texture, unreal.Texture2D):
            unreal.log(f"Processing texture: {asset.get_name()}, Compression: {texture.get_editor_property('compression_settings')}")
            if (asset.get_name().endswith("_n") or asset.get_name().endswith("_N")) and texture.get_editor_property('compression_settings') != unreal.TextureCompressionSettings.TC_NORMALMAP:
                unreal.log("Fixing compression settings for normal map")
                texture.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_NORMALMAP)
                
                unreal.EditorAssetLibrary.save_loaded_asset(texture)
        else:
            unreal.log("Not a texture: " + asset.get_name())
            
def clear_all_material_instance_params():
    EditorAssetLibrary = unreal.EditorAssetLibrary()
    MaterialEditingLibrary = unreal.MaterialEditingLibrary()
    assets_list = unreal.EditorUtilityLibrary().get_selected_assets()
    for asset in assets_list:
        material_instance = EditorAssetLibrary.load_asset(asset.get_path_name())
        
        if isinstance(material_instance, unreal.MaterialInstanceConstant):
            unreal.log(f"Processing material instance: {asset.get_name()}")
            MaterialEditingLibrary.clear_all_material_instance_parameters(material_instance)
        
            unreal.EditorAssetLibrary.save_loaded_asset(material_instance)
        else:
            unreal.log("Not a material instance: " + asset.get_name())
            
def set_material_instance_colors_to_red():
    EditorAssetLibrary = unreal.EditorAssetLibrary()
    MaterialEditingLibrary = unreal.MaterialEditingLibrary()
    assets_list = unreal.EditorUtilityLibrary().get_selected_assets()
    for asset in assets_list:
        material_instance = EditorAssetLibrary.load_asset(asset.get_path_name())
        
        if isinstance(material_instance, unreal.MaterialInstanceConstant):
            unreal.log(f"Processing material instance: {asset.get_name()}")
            params = MaterialEditingLibrary.get_vector_parameter_names(material_instance)
            for param in params:
                unreal.log(f"Setting parameter {param} to red")
                MaterialEditingLibrary.set_material_instance_vector_parameter_value(material_instance, param, unreal.LinearColor(1.0, 0.0, 0.0, 1.0))
            
            unreal.EditorAssetLibrary.save_loaded_asset(material_instance)
        else:
            unreal.log("Not a material instance: " + asset.get_name())

def remove_duplicated_static_mesh_actors():
    EditorActorLibrary = unreal.EditorActorSubsystem()
    actors = EditorActorLibrary.get_all_level_actors()
    staticMeshActors = []
    for actor in actors:
        if isinstance(actor, unreal.StaticMeshActor):
            staticMeshActors.append(actor)
            unreal.log(actor.get_name())
            
    for actor in staticMeshActors:
        for other_actor in staticMeshActors:
            if actor != other_actor and actor.get_actor_transform() == other_actor.get_actor_transform():
                unreal.log(f"Removed duplicated actor: {other_actor.get_name()}")
                unreal.EditorLevelLibrary.destroy_actor(other_actor)
                break
            
def print_all_static_mesh_fields():
    for item in dir(unreal.StaticMesh):
        print(item)
        
def print_all_static_mesh_fields_help():
    for item in dir(unreal.StaticMesh):
        print(help(item))
        
def print_edit_menu():
    menus = unreal.ToolMenus.get()
    edit_menu = menus.find_menu("LevelEditor.MainMenu")
    print(edit_menu)
    
def print_all_menus():
    menus = set()
    for i in range(1000):
        obj = unreal.find_object(None, "/Engine/Transient.ToolMenus_0:RegisteredMenu_%s" % i)
        if not obj:
            obj = unreal.find_object(None, f"/Engine/Transient.ToolMenus_0:RegisteredMenu_{i}")
            if not obj:
                continue
        
        menu_name = str(obj.menu_name)
        if (menu_name == "None"):
            continue
        
        menus.add(menu_name)
    for menu in menus:
        print(menu)
        
def return_value_to_blueprint():
    return True

def compute_slow_task():
    total_steps = 100
    dialog_name = "Slow task is working"
    with unreal.ScopedSlowTask(total_steps, dialog_name) as slow_task:
        slow_task.make_dialog(can_cancel=True)
        for i in range(total_steps):
            if slow_task.should_cancel():
                break
            slow_task.enter_progress_frame(1, f"Step {i + 1} of {total_steps}")
            time.sleep(0.1)  # Simulate some work being done

@unreal.uclass()
class MyScriptObject(unreal.ToolMenuEntryScript):
    @unreal.ufunction(override=True)
    def execute(self, context):
        print("SCRIPT EXECUTED")

def add_tool_menu():
    menus = unreal.ToolMenus.get()

    # CUSTOM SUBMENU
    main_menu = menus.find_menu("LevelEditor.MainMenu")
    if not main_menu:
        print("Failed to find the Main menu. Script terminated prematurely.")
        return
    custom_menu = main_menu.add_sub_menu("Custom Menu", "Python Automation", "Menu Name", "Menu Label")

    edit_menu = menus.find_menu("LevelEditor.MainMenu.Edit")
    if not edit_menu:
        print("Failed to find the Edit menu. Script terminated prematurely.")
        return

    # CUSTOM SCRIPT MENU ENTRY
    script_object = MyScriptObject()
    script_object.init_entry(
        owner_name=edit_menu.menu_name,
        menu=edit_menu.menu_name,
        section="EditMain",
        name="Custom tool",
        label="Custom tool",
        tool_tip="Custom Script Entry"
    )
    script_object.register_menu_entry()

def add_asset_context_menu():
    menus = unreal.ToolMenus.get()
    # CUSTOM SCRIPT CONTEXT MENU ENTRY
    asset_context_menu = menus.find_menu("ContentBrowser.AssetContextMenu.StaticMesh")
    script_object2 = MyScriptObject()
    script_object2.init_entry(
        owner_name=asset_context_menu.menu_name,
        menu=asset_context_menu.menu_name,
        section="GetAssetActions",
        name="Custom action",
        label="Custom action",
        tool_tip="Custom Script Entry"
    )
    script_object2.register_menu_entry()

    # REFRESH UI
    menus.refresh_all_widgets()
