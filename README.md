# ssdd24-25
Daniel Machuca Archidona

Daniel.Machuca@alu.uclm.es

**Instructions:**

For the execution of the project is needed to open a terminal tu run: remotetypes --Ice.Config=config/remotetypes.config

Once this is running, open a second terminal in order to execute the client.py (class implemented to test the functionality) located in: *ssdd-remote-types-main/remotetypes/client.py*

For running the test I've used pytest in the test folder as you proposed. I fixed the problem that led to the failure of one of the test  and added a few more test cases in a different class called *MoreTestStringSet* in the same script.

I've also used pylint in the different python scripts that I filled, in order to fix the possible problems that pylint suggested me to enhance, and incresing the quality of my code.

**second task:**

For this task I have installed Docker and Docker compose, besides Kafka-python and Kcat.

To start the app is necessary to start the docker service with the docker-compose.
Once I have a good docker image, use docker-compose up-d to start ssdd.remotetypes and kafka-entrypoint services.

I used to check the status with docker ps to be certain that kafka was healthy at any times

I created a script called kafkaClient.py that consume messages from an INPUT_TOPIC and publish the responsed in OUTPUT_TOPIC, conected with kafkas cluster with BOOTSTRAP_SERVERS and later connecting to the remote factory.

I also created a producer.py that send different messages that contains multiples operation to a topic, my client waits, listening the topic so it can process the operations received

**CLARIFICATIONS AFTER FEEDBACK**

in order to install docker, you need to run the next command:

$  sudo apt isntall docker.io docker-compose

For running the project you'll need to start your docker by running the next command in the directory where your yml is ubicated:

$ docker-compose up -d

and check if the service is up by:
$ docker ps

in another terminal you can start the project using a virtual enviroment: 
$ python3 -m venv venv

$ source venv/bin/activate

and next, installing the dependencies:

$ pip install kafka-python

and 

$ pip install .

When everything is installated and you have something like this:
❯ pip list
Package      Version
------------ --------
kafka-python 2.0.2
pip          22.0.2
remotetypes  0.1.0
setuptools   59.6.0
zeroc-ice    3.7.10.1

you are good to go

the way i have been executing the program is creating a venv and following the steps i just explained and, in a terminal y execute the kafkaClient.py and in another terminal I execute the proudcer.py:



