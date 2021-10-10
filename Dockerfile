FROM rasa/rasa:2.8.9-full

WORKDIR /app
COPY . . 

RUN rasa train nlu

# set the user 
USER 1001

# set entrypoint 
ENTRYPOINT ["rasa"]

# command when container is called to run
CMD ["run", "enable-api", "--port", "5005"]