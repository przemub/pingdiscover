FROM condaforge/miniforge3:4.10.3-1

RUN apt update && apt upgrade -y
# Required for doing anything with the network
RUN apt install -y netbase

WORKDIR /usr/src/app
COPY . .
RUN conda env create -f environment.yml

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "pingdiscover", "python", "-u", "pingdiscover.py"]

