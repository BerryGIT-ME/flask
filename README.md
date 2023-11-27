# Live links

front-end live url: https://ecommerce-chatbot-llm-front-end.vercel.app/

backend live url: https://flask-production-d89c.up.railway.app/

figma design url: https://www.figma.com/file/JVQWNLV8Umqwg3YFLMHyYa/Stutern-57?type=design&node-id=26-79&mode=design

loom walkthrough video: https://www.loom.com/share/3198a6e345af4be2af2c30a99fc9cfa9?sid=590ad1bf-33e4-44da-9e09-4ba5108752c3

Please not that ALL environment variables which includes database credentials and api keys are available in a google document file submitted as the project PRD.

# Installation

## Frontend

- Clone the [frontend](https://github.com/Stutern-E-commerce-AI-Application/ecommerce_chatbot_llm_front_end) repo
- cd into the repo directory
- There is no need to create a `.env` file for the front end as a `.env` file is present in the repo already. You may alter the value of the `REACT_APP_API_ENDPOINT` environment variable if by default the flask backend does not run in the specified ip address and port
- install the packages - `npm install`
- start the dev server - `npm start`

## Backend

- Clone the [backend](https://github.com/Stutern-E-commerce-AI-Application/flask) repo
- cd into the repo directory
- We strongly recommend that you check out the `with-image-search` branch of the repo. This branch contains updated code and packages for running the app in multimodal configuration. Check the notes about our desigh section to see the justification for this. TLDR - image size too large to deploy.
- use the sample.env as a template and create a `.env` file.
- Populate the `.env` file with data available in the google docs shared as the project PRD during submission
- (optional) Create a python environment - `python -m venv env` or `python3 -m venv env`

- (optional) Activate the environment - `source env/bin/activate` not this is for a unix based os e.g linux and mac
- install the packages - `pip install -r requirements.txt`
- start the dev server - `python main.py`

Please note that when testing locally, the web app requres that backend server be at `http://127.0.0.1:5000` if the flask app is started with a different Ip address please update the `REACT_APP_API_ENDPOINT` environment variable in the `.env` file of the front end repo to the ip addesss of the flask server and restart the web app - make sure to follow the format already existing in the `.env` file.

# Important notes about the design

The video walkthrough demoed a version of this application that is capable of handling multimodal data - You can upload images to the chat bot and get products that are similar from the database. We felt that adding this was a huge step to bridging the gap between complex data managment and an intuitive user experience.

However implementing that solution involvs deploying a image transformer locally and using that for generating embeddings for media files. This results in a really large build size which we were unable to deploy with our current cloud host provider even after paying for a higer tier. As a result the demo shown was of a version of the application that is in the `with-image-search` branch.
