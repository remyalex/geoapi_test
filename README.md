# geoapi_test
**Sample GeoAPI test for PNN**

* *DOCKER Build*
  Since cloned, enter repository dir and execute:
  ```bash
  $ docker build -t geoapi:latest .
  >... (geoapi must be builded)
  $ docker images
  >... list of images (geoapi listed)
  $ docker run -p 5000:5000 geoapi
  >... server output
  ```
  
