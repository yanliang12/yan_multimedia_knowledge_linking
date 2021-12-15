############Dockerfile###########
FROM openjdk:8

RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install -y git 
RUN apt-get install -y curl
RUN apt-get install -y vim
RUN apt-get install -y tar

RUN apt-get install -y python3-dev
RUN apt-get install -y python3-pip

####neo4j
RUN pip3 install neo4j==4.1.1
RUN wget http://neo4j.com/artifact.php?name=neo4j-community-3.5.12-unix.tar.gz
RUN tar -xf 'artifact.php?name=neo4j-community-3.5.12-unix.tar.gz'
WORKDIR /neo4j-community-3.5.12/
RUN echo "dbms.security.auth_enabled=false" > /neo4j-community-3.5.12/conf/neo4j.conf
RUN echo "dbms.connectors.default_listen_address=0.0.0.0" >> /neo4j-community-3.5.12/conf/neo4j.conf
RUN echo "dbms.connector.http.address=0.0.0.0:7474" >> /neo4j-community-3.5.12/conf/neo4j.conf
EXPOSE 7474
EXPOSE 7687
WORKDIR /

####dexter 
RUN pip3 install requests==2.24.0
RUN wget http://dexter.isti.cnr.it/dexter.tar.gz
RUN apt-get install -y tar
RUN tar xvzf dexter.tar.gz
RUN mv /dexter2/* ./
EXPOSE 8080
WORKDIR /

####sparql
RUN pip3 install gdown
RUN pip3 install rdflib==5.0.0
RUN pip3 install requests==2.24.0
WORKDIR /

####flask
WORKDIR /
RUN pip3 install Werkzeug==0.16.1
RUN pip3 install flask==1.1.2
RUN pip3 install flask_restplus==0.13.0
RUN git clone https://github.com/gaoyuanliang/jessica_flusk.git
RUN mv jessica_flusk/* ./
EXPOSE 9000
WORKDIR /

####easyocr
RUN pip3 install easyocr==1.1.10
RUN apt-get install -y libgl1-mesa-dev
RUN python3 -c "import easyocr;reader = easyocr.Reader(['en'])"
WORKDIR /

###deepseech
RUN pip3 install deepspeech==0.8.2
RUN pip3 install webrtcvad==2.0.10
RUN pip3 install pyqt5==5.9.1
RUN apt-get install -y sox
RUN apt-get install -y ffmpeg
RUN curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.8.1/deepspeech-0.8.1-models.pbmm
RUN curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.8.1/deepspeech-0.8.1-models.scorer
RUN git clone https://github.com/yanliang12/DeepSpeech-examples.git
RUN mv /DeepSpeech-examples/vad_transcriber/* ./
WORKDIR /

###stanza
RUN pip3 install stanza==1.1.1
RUN python3 -c "import stanza;stanza.download('en')"

###download the ttl files
#entity linking
RUN gdown https://drive.google.com/uc?id=19A9dmnwz3w09hrgL4aDzgaDiNvLHHnk-
RUN gdown https://drive.google.com/uc?id=1K2_4J4z28BxoFrfGE94d2LTtAWFwNJA_

##########
#sparql small
RUN gdown https://drive.google.com/uc?id=1Acef8AzY5sGNYViAHU9p2bBcfxEnmndC
RUN gdown https://drive.google.com/uc?id=1iKkzwZsmTBBbk8O351qQp-hb3dV3yOB7

#sparql tinny
#RUN gdown https://drive.google.com/uc?id=12Czx5XjkS7cpkKLKLiI3Kf3Xt0KdnrSk
#RUN gdown https://drive.google.com/uc?id=10j7V2YW5Oxda-Iy3VYzfCqKY0uVHGUg_

###download the codes
RUN echo "sdhdkgfy"
WORKDIR /

RUN git clone https://github.com/yanliang12/yan_ner_docker.git
RUN mv /yan_ner_docker/* ./
RUN rm -r yan_ner_docker

RUN git clone https://github.com/yanliang12/yan_ocr.git
RUN mv /yan_ocr/* ./
RUN rm -r yan_ocr

RUN git clone https://github.com/yanliang12/yan_docker_speech_to_text.git
RUN mv /yan_docker_speech_to_text/* ./
RUN rm -r yan_docker_speech_to_text

RUN git clone https://github.com/gaoyuanliang/jessica_dbpedia_sparql_docker.git
RUN mv jessica_dbpedia_sparql_docker/* ./
RUN rm -r jessica_dbpedia_sparql_docker

RUN git clone https://github.com/gaoyuanliang/jessica_entity_linking_docker.git
RUN mv jessica_entity_linking_docker/* ./
RUN rm -r jessica_entity_linking_docker

RUN git clone https://github.com/yanliang12/yan_neo4j_docker.git
RUN mv /yan_neo4j_docker/* ./
RUN rm -r yan_neo4j_docker

RUN git clone https://github.com/gaoyuanliang/jessica_knowledge_linking.git
RUN mv jessica_knowledge_linking/* ./
RUN rm -r jessica_knowledge_linking

RUN rm Dockerfile*

CMD python3 app_path.py
############Dockerfile###########
