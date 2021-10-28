# Virtual-Assistant-Team-2-Dell-H2H-Chatbot

## Installation
```sh
git clone https://github.com/manavendrasen/Virtual-Assistant-Dell-H2H-Chatbot
cd Virtual-Assistant-Dell-H2H-Chatbot
```

### Run the server
After activating the enviornment and installing rasa, requests in the dev env.

1. Train the modal
```sh
rasa train 
```

2. Start the action server
```sh
rasa run actions
```

3. Start Duckling for Entity Extration
```sh
docker run -p 8000/8000 rasa/duckling
```

4. Start RASA server
```sh
rasa run -m models --enable-api --cors “*” --debug
```

Open frontend to test the bot: https://github.com/manavendrasen/Virtual-Assistant-Dell-H2H-Frontend
