import unreal
import configparser
import os

class StaticMeshValidator:
    def __init__(self):
        # Загрузка конфигурационного файла
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), '..', 'AssetValidationConfig.ini'))
        
        # Загрузка параметров из конфигурационного файла
        self.max_vertices_first_lod = config.getint('StaticMeshValidator', 'MaxVerticesFirstLod')
        self.max_vertices_last_lod = config.getint('StaticMeshValidator', 'MaxVerticesLastLod')
        self.max_material_slots = config.getint('StaticMeshValidator', 'MaxMaterialSlots')
        self.max_lods = config.getint('StaticMeshValidator', 'MaxLods')
        self.max_collision_primitives = config.getint('StaticMeshValidator', 'MaxCollisionPrimitives')
        self.max_uv_channels = config.getint('StaticMeshValidator', 'MaxUVChannels')
        self.max_mesh_volume = config.getfloat('StaticMeshValidator', 'MaxMeshVolume')
        self.max_mesh_size = config.getfloat('StaticMeshValidator', 'MaxMeshSize')
        self.is_nanite = config.getboolean('StaticMeshValidator', 'IsNanite')
        self.has_lightmap = config.getboolean('StaticMeshValidator', 'HasLightmap')
        self.has_complex_collision = config.getboolean('StaticMeshValidator', 'HasComplexCollision')
        self.has_distance_field = config.getboolean('StaticMeshValidator', 'HasDistanceField')
        self.non_geometry_material_slots = config.get('StaticMeshValidator', 'NonGeometryMaterialSlots').split(',')
        self.default_material_name = config.get('StaticMeshValidator', 'DefaultMaterialName')

    def can_validate(self, asset):
        return isinstance(asset, unreal.StaticMesh)

    def validate(self, asset, mark_asset_error):
        unreal.log(f"Validating: {asset.get_name()}")
        self.check_vertices(asset, mark_asset_error)
        self.check_material_slots(asset, mark_asset_error)
        self.check_duplicate_materials(asset, mark_asset_error)
        self.check_lods(asset, mark_asset_error)
        #self.check_collision_primitives(asset, mark_asset_error)
        #self.check_uv_channels(asset, mark_asset_error)
        #self.check_mesh_volume(asset, mark_asset_error)
        #self.check_mesh_size(asset, mark_asset_error)
        #self.check_nanite_support(asset, mark_asset_error)
        #self.check_lightmap(asset, mark_asset_error)
        #self.check_complex_collision(asset, mark_asset_error)
        #self.check_distance_field(asset, mark_asset_error)
        #self.check_non_geometry_material_slots(asset, mark_asset_error)
        #self.check_default_material(asset, mark_asset_error)

    def check_vertices(self, asset, mark_asset_error):
        smes = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
        lods = smes.get_lod_count(asset)
        if lods > 0:
            first_lod_vertices = smes.get_number_verts(asset, 0)
            unreal.log(f"Checking vertices: First LOD has {first_lod_vertices} vertices.")
            if first_lod_vertices > self.max_vertices_first_lod:
                mark_asset_error(asset, f"has {first_lod_vertices} vertices in the first LOD, which exceeds the limit of {self.max_vertices_first_lod}.")
        if lods > 1:
            last_lod_vertices = smes.get_number_verts(asset, lods - 1)
            unreal.log(f"Checking vertices: Last LOD has {last_lod_vertices} vertices.")
            if last_lod_vertices > self.max_vertices_last_lod:
                mark_asset_error(asset, f"has {last_lod_vertices} vertices in the last LOD, which exceeds the limit of {self.max_vertices_last_lod}.")

    def check_material_slots(self, asset, mark_asset_error):
        smes = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
        material_slots = smes.get_number_materials(asset)
        unreal.log(f"Checking material slots: Asset has {material_slots} material slots.")
        if material_slots > self.max_material_slots:
            mark_asset_error(asset, f"has {material_slots} material slots, which exceeds the limit of {self.max_material_slots}.")

    def check_duplicate_materials(self, asset, mark_asset_error):
        smes = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
        materials = [smes.get_lod_material_slot(asset, 0, i) for i in range(smes.get_number_materials(asset))]
        unreal.log(f"Checking duplicate materials: Asset has {len(materials)} materials.")
        if len(materials) != len(set(materials)):
            mark_asset_error(asset, "has duplicate materials.")

    def check_lods(self, asset, mark_asset_error):
        smes = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
        lods = smes.get_lod_count(asset)
        unreal.log(f"Checking LODs: Asset has {lods} LODs.")
        if lods > self.max_lods:
            mark_asset_error(asset, f"has {lods} LODs, which exceeds the limit of {self.max_lods}.")

    def check_collision_primitives(self, asset, mark_asset_error):
        smes = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
        collision_primitives = smes.get_number_collision_primitives(asset)
        unreal.log(f"Checking collision primitives: Asset has {collision_primitives} collision primitives.")
        if collision_primitives > self.max_collision_primitives:
            mark_asset_error(asset, f"has {collision_primitives} collision primitives, which exceeds the limit of {self.max_collision_primitives}.")

    def check_uv_channels(self, asset, mark_asset_error):
        uv_channels = asset.get_num_uv_channels()
        unreal.log(f"Checking UV channels: Asset has {uv_channels} UV channels.")
        if uv_channels > self.max_uv_channels:
            mark_asset_error(asset, f"has {uv_channels} UV channels, which exceeds the limit of {self.max_uv_channels}.")

    def check_mesh_volume(self, asset, mark_asset_error):
        bounds = asset.get_bounds()
        volume = bounds.box_extent.x * bounds.box_extent.y * bounds.box_extent.z * 8  # Volume of the bounding box
        unreal.log(f"Checking mesh volume: Asset has volume {volume}.")
        if volume > self.max_mesh_volume:
            mark_asset_error(asset, f"has a volume of {volume}, which exceeds the limit of {self.max_mesh_volume}.")

    def check_mesh_size(self, asset, mark_asset_error):
        bounds = asset.get_bounds()
        max_size = max(bounds.box_extent.x, bounds.box_extent.y, bounds.box_extent.z) * 2  # Max size along any axis
        unreal.log(f"Checking mesh size: Asset has max size {max_size}.")
        if max_size > self.max_mesh_size:
            mark_asset_error(asset, f"has a size of {max_size} along its bounds axes, which exceeds the limit of {self.max_mesh_size}.")

    def check_nanite_support(self, asset, mark_asset_error):
        nanite_enabled = asset.is_nanite_enabled()
        unreal.log(f"Checking Nanite support: Asset Nanite enabled is {nanite_enabled}.")
        if nanite_enabled != self.is_nanite:
            mark_asset_error(asset, f"Nanite support mismatch: expected {self.is_nanite}, found {nanite_enabled}.")

    def check_lightmap(self, asset, mark_asset_error):
        lightmap_uv = asset.has_lightmap_uv()
        unreal.log(f"Checking Lightmap UVs: Asset Lightmap UVs is {lightmap_uv}.")
        if lightmap_uv != self.has_lightmap:
            mark_asset_error(asset, f"Lightmap UVs mismatch: expected {self.has_lightmap}, found {lightmap_uv}.")

    def check_complex_collision(self, asset, mark_asset_error):
        collision_complexity = asset.get_collision_complexity()
        unreal.log(f"Checking complex collision: Asset collision complexity is {collision_complexity}.")
        if self.has_complex_collision:
            if collision_complexity not in [unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE, unreal.CollisionTraceFlag.CTF_USE_SIMPLE_AND_COMPLEX]:
                mark_asset_error(asset, f"Complex collision required but found {collision_complexity}.")

    def check_distance_field(self, asset, mark_asset_error):
        distance_field = asset.generate_distance_field_as_if_two_sided()
        unreal.log(f"Checking distance field: Asset distance field is {distance_field}.")
        if distance_field != self.has_distance_field:
            mark_asset_error(asset, f"Distance field generation mismatch: expected {self.has_distance_field}, found {distance_field}.")

    def check_non_geometry_material_slots(self, asset, mark_asset_error):
        materials = [asset.get_material(i) for i in range(asset.get_num_materials())]
        unreal.log(f"Checking non-geometry material slots: Asset has {len(materials)} materials.")
        for material in materials:
            if material.get_name() in self.non_geometry_material_slots:
                mark_asset_error(asset, f"Material slot {material.get_name()} is not associated with geometry.")

    def check_default_material(self, asset, mark_asset_error):
        materials = [asset.get_material(i) for i in range(asset.get_num_materials())]
        unreal.log(f"Checking default material: Asset has {len(materials)} materials.")
        for material in materials:
            if material.get_name() == self.default_material_name:
                mark_asset_error(asset, f"contains the default material {self.default_material_name} in one of its slots.")

