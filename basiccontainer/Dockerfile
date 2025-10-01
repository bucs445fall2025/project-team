FROM python:3.12

# NOTE: RUN ON HOST
# RUN echo "vm.overcommit_memory = 1" >> /etc/sysctl.conf && sysctl -p
#WORKDIR /var/app
EXPOSE 5000

RUN apt-get update && apt-get install --no-install-recommends -y \
	build-essential curl git && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

# install dependencies

RUN pip install --no-cache-dir --upgrade pip wheel
COPY ./requirements.txt /var/tmp/requirements.txt
RUN pip install -r /var/tmp/requirements.txt
#ENV FLASK_APP=app.py

COPY ./app.py /var/app/app.py
#CMD ["flask", "run", "--host=0.0.0.0"]