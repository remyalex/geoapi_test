import os
from flask import Flask, jsonify, send_from_directory
from flask_restful import Resource, Api
from datetime import datetime
import pandas as pd
import geopandas as gp
import matplotlib.pyplot as plt
import zipfile

app = Flask(__name__)

UPLOAD_DIRECTORY = "./geoprocess_files"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
urlDptos = "https://services1.arcgis.com/flBhk9lC6HvZV0Sw/ArcGIS/rest/services/Deptos_SINAP/FeatureServer/0/query?where=1%3D1&geometryType=esriGeometryEnvelope&spatialRel=esriSpatialRelIntersects&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&returnZ=false&returnM=false&returnExceededLimitFeatures=true&sqlFormat=none&f=pgeojson"
urlRunap = "https://services1.arcgis.com/flBhk9lC6HvZV0Sw/ArcGIS/rest/services/RUNAP/FeatureServer/0/query?where=1%3D1&geometryType=esriGeometryEnvelope&spatialRel=esriSpatialRelIntersects&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&returnZ=false&returnM=false&returnExceededLimitFeatures=true&sqlFormat=none&f=pgeojson"

@app.route("/files")
def list_files():
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)

@app.route("/files/<path:path>")
def get_file(path):
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

api = Api(app)

class Intersect(Resource):
    def get(self, filename):
        self.logs = []
        dptosDF = gp.read_file(urlDptos)
        dr = str(datetime.now()) + ' - (GET) DptosSINAP feats: ' + str(len(dptosDF))
        print (dr)
        self.logs.append(dr)
        runapDF = gp.read_file(urlRunap)
        rr = str(datetime.now()) + ' - (GET) RUNAP feats: ' + str(len(runapDF))
        print (rr)
        self.logs.append(rr)
        intDF = gp.overlay(runapDF, dptosDF, how='intersection')
        df = pd.DataFrame({
            'area_HAs': intDF.to_crs("EPSG:3395").geometry.area*0.0001,
            'id_pnn': intDF['id_pnn'],
            'name_pnn': intDF['nombre'],
            'name_dpto': intDF['NOMBRE_DEP']
        })
        gdf = gp.GeoDataFrame(df, geometry=intDF.geometry)
        gpLog = str(datetime.now()) + ' - (GeoProccess) '+ filename +' feats: ' + str(len(gdf))
        print (gpLog)
        self.logs.append(gpLog)
        gdf.to_file(UPLOAD_DIRECTORY+'/'+filename+'.shp')
        zF = self.ZipShape(UPLOAD_DIRECTORY+'/'+filename+'.shp')
        gpOut = {
            "GP_date": str(datetime.now()),
            "GP_logs": self.logs,
            "Intersection_length":len(gdf),
            "File_url": '/files/' + os.path.split(zF.filename)[1]
        }
        return gpOut

    def ZipShape(self, path):
        path, name = os.path.split(path)
        zip_path = os.path.join(path, name.split('.')[0] +'_'+datetime.now().strftime('%Y%m%d%H%M%S') + '.zip')
        zip = zipfile.ZipFile(zip_path, 'w')
        for f in os.listdir(path):
            if os.path.isfile(os.path.join(path,f)) and not f.endswith('.zip'):
                zip.write(os.path.join(path,f), f)
                os.remove(os.path.join(path,f))
        zip.close()
        return zip

class PrintMap(Resource):
    def get(self, filename):
        runapDF = gp.read_file(urlDptos)
        print (str(datetime.now()) + ' - (GET) RUNAP feats: ' + str(len(runapDF)))
        runapDF.plot()
        plt.savefig(UPLOAD_DIRECTORY+'/'+filename+'.jpg')
        return send_from_directory(UPLOAD_DIRECTORY, filename+'.jpg', as_attachment=False)

api.add_resource(Intersect, '/intersect/<filename>')
api.add_resource(PrintMap, '/printMap/<filename>')

if __name__ == '__main__':
 app.run(debug=True, host='0.0.0.0')
