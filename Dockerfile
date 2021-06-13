# Sets the base image 
#FROM python:3
FROM continuumio/miniconda3

# set the working directory for containers
WORKDIR /usr/src/mnist

# Copy the source files to the working directory
COPY requirements.txt .
COPY models/ ./models
COPY src/ ./src

# list workdir
RUN ls -laR .

# install build utilities
RUN apt-get -y update
#RUN pip install -r requirements.txt
RUN conda config --append channels conda-forge
RUN conda install --file requirements.txt

# check our python environment
RUN python --version
#RUN pip --version
RUN conda --version

#Expose the required port
EXPOSE 5000

# Command to run on container start
CMD [ "python", "./src/app.py" ]
