# geoapi_test
**Sample GeoAPI test for PNN**

## *DOCKER Build*:
  
  Once cloned, enter repository dir and execute:
  ```bash
  $ docker build -t geoapi:latest .
  >... (geoapi must be builded)
  $ docker images
  >... list of images (geoapi listed)
  $ docker run -p 5000:5000 geoapi
  >... server output
  ```
## *Python virtualenv Build*:
  
  OS Requeriments:
  * Python=>3.5
  * Pip=>20
  * virtualenv => A guide to install and create envs: [Virtualenv Python](https://gist.github.com/Geoyi/d9fab4f609e9f75941946be45000632b)
  
  Activate created venv and execute (on geoapi path):
   ```bash
  $ pip install -r requeriments.txt
  >... (Dependecies must be installed)
  $ python geoapy.py
  >... geoapi output
  ```
  
## *Usage*:
    This API application is build in Python with Flask microframework (v1.1.1) as entry point. The routes of this api indicates the operation or geoprocess to execute:
    * Intersect (http://localhost:5000/intersect/<outFileName>)
    * PrintMap (http://localhost:5000/printMap/<outFileName>)

    A static route is then defined as output directory in which, every output geoprocess files are saved:
    * Files (http://localhost:5000/files/)
    
    If want to dowload a execution result, al you have to do is to access to file path: (http://localhost:5000/files/<outFileName>).
    
    Parameter <outFileName> obtained after a Geoprocess execution (File_url).
    
