FROM wooyek/geodjango
ENV PYTHONBUFFERED 1

# Install GDAL dependencies
RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin

# Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal



#RUN export LD_LIBRARY_PATH=/lib:$LD_LIBRARY_PATH
#RUN chmod a+rwx  -R /lib/

# add init script
CMD ["./initdb-postgis.sh"]

RUN echo "Here we are"

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt
COPY . /code/


