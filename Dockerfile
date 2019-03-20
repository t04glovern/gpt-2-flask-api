FROM ubuntu:18.04

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

COPY ["environment.yml", "/root/environment.yml"]

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
libglib2.0-0 libxext6 libsm6 libxrender1 \
git mercurial subversion python-dev gcc

# install miniconda and python 3.7
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-4.5.11-Linux-x86_64.sh -O ~/miniconda.sh && \
/bin/bash ~/miniconda.sh -b -p /opt/conda && \
rm ~/miniconda.sh && \
ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc

RUN /opt/conda/bin/conda env create -f=/root/environment.yml -n ml-flask
RUN echo "conda activate ml-flask" >> ~/.bashrc
SHELL ["/bin/bash", "-c", "source ~/.bashrc"]
RUN conda activate ml-flask

COPY ["deployment", "/usr/src/app/deployment"]
COPY ["models", "/usr/src/app/models"]

WORKDIR /usr/src/app/deployment
CMD [ "/bin/bash" ]
