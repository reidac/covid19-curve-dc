# From the Galileo app examples.

FROM python:3.7

ENV FIG_PATH /usr/local

#The next block determines what dependencies to load

RUN pip3 install numpy
RUN pip3 install matplotlib
RUN pip3 install scipy
RUN pip3 install pandas
RUN pip3 install requests

COPY . .

#The entrypoint is the command used to start your project

ENTRYPOINT ["python3","exponential.py"]
