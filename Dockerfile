# Sets the base image 
FROM continuumio/miniconda3

# set the working directory for containers
WORKDIR /usr/src/movielens

# Copy the source files to the working directory
COPY requirements.txt .
COPY data/ ./data
COPY model/ ./model
COPY src/ ./src

# list workdir
RUN ls -laR .

# install build utilities
RUN apt-get -y update
RUN conda config --append channels conda-forge
RUN conda install --file requirements.txt

# check our python environment
RUN python --version
RUN conda --version

#Expose the required port
EXPOSE 5000

# Command to run on container start
CMD [ "python", "-u", "./src/train.py" ]
