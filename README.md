# geoapi_test
**Sample GeoAPI test for PNN**

* *DOCKER Build*:
  Since cloned, enter repository dir and execute:
  ```bash
  $ docker build -t geoapi:latest .
  >... (geoapi must be builded)
  $ docker images
  >... list of images (geoapi listed)
  $ docker run -p 5000:5000 geoapi
  >... server output
  ```
* *Python virtualenv Build*:
  OS Requeriments:
  * Python=>3.5
  * Pip=>20
  * virtualenv => A guide to install and create envs: [Virtualenv Python](https://gist.github.com/Geoyi/d9fab4f609e9f75941946be45000632b){:target="_blank"}
  
  Activate created venv and execute (on geoapi path):
   ```bash
  $ pip install -r requeriments.txt
  >... (Dependecies must be installed)
  $ python geoapy.py
  >... (geoapi output)
  ```
  
