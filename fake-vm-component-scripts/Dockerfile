FROM qubell/python-scripting

RUN mkdir /vms && mkdir /volumes
RUN pip3 install click

ADD /fake-vm/*.py /fake-vm/
ADD /fake-volume/*.py /fake-volume/
