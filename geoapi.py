from flask import Flask, send_from_directory
from flask_restful import Resource, Api
import geopandas
from datetime import datetime

app = Flask(__name__)
api = Api(app)

class Intersect(Resource):
    def get(self, filename):
        urlDptos = "https://services1.arcgis.com/flBhk9lC6HvZV0Sw/ArcGIS/rest/services/Deptos_SINAP/FeatureServer/0/query?where=1%3D1&geometryType=esriGeometryEnvelope&spatialRel=esriSpatialRelIntersects&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&returnZ=false&returnM=false&returnExceededLimitFeatures=true&sqlFormat=none&f=pgeojson"
        dptosDF = geopandas.read_file(urlDptos)
        print (str(datetime.now()) + ' - (GET) DptosSINAP feats: ' + str(len(dptosDF)))
        urlRunap = "https://services1.arcgis.com/flBhk9lC6HvZV0Sw/ArcGIS/rest/services/RUNAP/FeatureServer/0/query?where=1%3D1&geometryType=esriGeometryEnvelope&spatialRel=esriSpatialRelIntersects&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&returnZ=false&returnM=false&returnExceededLimitFeatures=true&sqlFormat=none&f=pgeojson"
        runapDF = geopandas.read_file(urlRunap)
        print (str(datetime.now()) + ' - (GET) RUNAP feats: ' + str(len(runapDF)))
        intDF = geopandas.overlay(runapDF, dptosDF, how='intersection')
        print (str(datetime.now()) + ' - (GeoProccess) '+ filename +' feats: ' + str(len(intDF)))
        intDF.to_file(filename+'.geojson', driver='GeoJSON')
        return {filename + "_length":len(intDF), "File": send_from_directory('./', filename+'.geojson', as_attachment=True)} #intDF.to_json()

api.add_resource(Intersect, '/intersect/<filename>')

if __name__ == '__main__':
 app.run(debug=True, host='0.0.0.0')
