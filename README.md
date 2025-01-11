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

To start the app is necessary to start the docker service with the docker-compose.yml.
Once I have a good docker image, use docker-compose up-d to start ssdd.remotetypes and kafka-entrypoint services.

I used to check the status with docker ps to be certain that kafka was healthy at any times

I created a script called kafkaClient.py that consume messages from an INPUT_TOPIC and publish the responsed in OUTPUT_TOPIC, conected with kafkas cluster with BOOTSTRAP_SERVERS and later connecting to the remote factory.

I also created a producer.py that send different messages that contains multiples operation to a topic, my client waits, listening the topic so it can process the operations received

