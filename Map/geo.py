import pandas as pd
from geojson import MultiPoint
import json

df=pd.read_csv('Map\ML_2022-03-13T00-44_monpar_photo.csv')



geo_json=df.reindex(columns=['ML Catalog Number','Latitude','Longitude']).rename(columns={'ML Catalog Number':'IDs'})
print(geo_json.columns)
list=[]

for row in geo_json.itertuples():
    data={
        "type": "Feature",
        "properties": {
        "name": row.IDs,
        
        "popupContent": "Monk Parakeet"
            },
        "geometry": {
        "type": "Point",
        "coordinates": [row.Latitude, row.Longitude]
                    }
            }
    list.append(data)
with open("Geo.json", "w") as data_file:
    json.dump(list,data_file)    
# json.dump(list, data_file, indent = 4)
        



    



# from geojson import Feature, FeatureCollection, Point

# features = []


# collection = FeatureCollection(features)
# with open("GeoObs.json", "w") as f:
#     f.write('%s' % collection)

# for latitude, longitude in geo_json:
#     latitude, longitude = map(float, (latitude, longitude))
#         features.append(
#             Feature(
#                 geometry = Point((longitude, latitude)),
#                 properties = {
#                     'weather': weather,
#                     'temp': temp
#                 }
    
