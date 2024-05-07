from pyproj import Proj, Transformer

# Define the projection for EPSG:26918 (NAD83 / UTM zone 18N) and EPSG:4326 (WGS84)
in_proj = 'epsg:26918'
out_proj = 'epsg:4326'
transformer_26_43 = Transformer.from_proj(in_proj, out_proj)
transformer_43_26 = Transformer.from_proj(out_proj, in_proj)
# List of points in EPSG:26918
points_epsg_26918 = [
    (586296.569209, 4512497.862743),
    (583324.4866324601, 4506805.373160211),
    (583304.1823994748, 4506069.654048115),
    (590250.10594797, 4518558.019924332),
    (590454.7399891173, 4519145.719617855),
    (590465.8934191109, 4519168.697483203),
    (590573.169495527, 4520214.766177284),
    (591252.8314104103, 4520950.353355553),
    (590946.3972262995, 4521077.318976877),
    (591583.6111452815, 4521434.846626811)
]

points_espg_4326 = [
    (40.745118134017304, -74.00187205105942),
    (40.726067710166404, -73.9784016322516)

]
# Convert each point and print the longitude, latitude
for x, y in points_epsg_26918:
    lat, lon = transformer_26_43.transform(x, y)
    print(f"lat: {lat}, long: {lon}")

for x, y in points_espg_4326:
    x, y = transformer_43_26.transform(x, y)
    print(f"x: {x}, y: {y}")