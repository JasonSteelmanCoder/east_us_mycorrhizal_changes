# This file should be run inside of your ArcGIS Pro instance.
# replace {os.getenv("MS_USER_NAME")} with your username on windows computers

import arcpy

workspace = f"C:/Users/{os.getenv("MS_USER_NAME")}/Documents/ArcGIS/Projects/regions_exploration/regions_exploration.gdb"
arcpy.env.workspace = workspace

regions = "S_USA_EcomapProvinces_ExportFeatures_ClipLayer"
counties = "east_us_shapefile_region_ExportFeatures"
output_feature_class = "east_us_counties_by_region"

arcpy.management.CopyFeatures(counties, output_feature_class)
arcpy.management.AddField(output_feature_class, "region_id", "TEXT")

arcpy.analysis.SpatialJoin(
    target_features = output_feature_class,
    join_features = regions,
    out_feature_class = r"memory/spatial_join",
    match_option = "LARGEST_OVERLAP"
)

field_names = [f.name for f in arcpy.ListFields(r"memory/spatial_join")]

intersection_dict = {}
with arcpy.da.SearchCursor(r"memory/spatial_join", ["TARGET_FID", "MAP_UNIT_N", "Shape_Area"]) as cursor:
    for target_fid, map_unit_n, shape_area in cursor:
        if target_fid not in intersection_dict or shape_area < intersection_dict[target_fid][1]:
            intersection_dict[target_fid] = (map_unit_n, shape_area)
            
with arcpy.da.UpdateCursor(output_feature_class, ["OBJECTID", "region_id"]) as cursor:
    for objectid, region_id in cursor:
        if objectid in intersection_dict:
            cursor.updateRow([objectid, intersection_dict[objectid][0]])
            
arcpy.management.Delete(r"memory/spatial_join")