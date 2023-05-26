## Telnyx SMS Guidelines Documentation Assistant

An AI chatbot built with LangChain, OpenAI GPT-3.5 and a Streamlit UI that can assist customers with the guidelines for sending SMS to each country with Telnyx.

The Streamlit app is available at: https://umbertoselva-telnyx-sms-guidelines-assistant-app-1av2vi.streamlit.app

#### How to run on your local machine

1. Download the Github repo on your local machine
2. Open a terminal and navigate to the Telnyx-SMS-Guidelines-Assistant folder
3. Create a hidden streamlit folder with a secrets.toml file in it
    ```
    mkdir .streamlit
    cd .streamlit
    touch secrets.toml
    ```
4. Open the secrets.toml file (e.g. with `nano secrets.toml`) and store your OpenAI API Key in it. Your file content should look as follows:
    ```
    OPENAI_API_KEY="paste-your-openai-api-key-here"
    ```
5. Navigate back to the Telnyx-SMS-Guidelines-Assistant folder, create a dedicated virtual environment, activate it, and install the dependencies from the requirements.txt file
    ```
    python -m venv venv_telnyx_assistant
    source venv_telnyx_assistant/bin/activate
    pip install -r requirements.txt
    ```
6. Run the following command to launch the Streamlit app in your browser
    ```
    streamlit run app.py
    ```
    
#### Development and alternative ideas

In order to demonstrate the chatbot functionalities, I decided to build a Streamlit app (see [app.py](https://github.com/umbertoselva/Telnyx-SMS-Guidelines-Assistant/blob/main/app.py)). An alternative solution could have been to set up an API route to respond to the user questions via requests.

I decided to carry out the documentation preprocessing part as well as the ingestion of the data into a vectorstore (see [preprocessing.ipynb](https://github.com/umbertoselva/Telnyx-SMS-Guidelines-Assistant/blob/main/preprocessing.ipynb) and [ingest.ipynb](https://github.com/umbertoselva/Telnyx-SMS-Guidelines-Assistant/blob/main/ingest.ipynb) — I worked on both notebooks in Google Colab) separately from the app itself. The app thus relies on the resulting vectorstore.pkl file. Alternatively it would be possible to include a pipeline that automates the preprocessing and the creation of a vectorstore upon a POST request (e.g. by adding an API route that calls a function from a separate ingest.py file containing such pipeline), allowing, for instance, to quickly have the chatbot work with an updated version of the documentation.

#### Challenges I faced during the development

I initially built the chatbot to work with the given documentation.json file as such, but soon realized that many of the performance issues could be solved by performing some data cleaning on the dataset (e.g. removing duplicates, removing HTML tags, etc. — please see the [preprocessing.ipynb](https://github.com/umbertoselva/Telnyx-SMS-Guidelines-Assistant/blob/main/preprocessing.ipynb) file). The alternative, i.e. to try and adapt the chatbot to a non-ideal dataset seemed less appealing and practical a strategy to me.

The chatbot performs well on the given test questions (see below) and also on non-pertinent questions (it will apologise for not knowing the answer, ask the user to reformulate, etc.). However, it fails test question number 3 ("What is the MCC for Serbia?"). It appears that the retrieved contexts include various info on other Balkan countries, but not Serbia's information. I have not been able to figure out why yet, nor to observe any other case in which it fails in a similar fashion. It might be useful to test different retrievers or embeddings (although this might affect the performance in other ways).

#### Test questions

Of the given test questions, the chatbot only fails to answer question n.3.

1. What are the SMS Guidelines for Ireland?
    > The SMS guidelines for Ireland are as follows: MCC is 272, Dial Code is 353, Alphanumeric Sender IDs are supported and will be maintained, no registration is required, and there are no restrictions with regards to content towards this destination. Please make sure to always refer to our Acceptable Use Policy for Messaging.
2. What country uses the country code 52?
    > Mexico uses the country code 52.
3. What is the MCC for Serbia?
    > Unfortunately, I don't know the answer to this question. Please reformulate it or ask something different.
4. Is alphanumeric SMS supported in China?
    > No, Alphanumeric Sender IDs are not supported for SMS in China. All Alphanumeric Sender IDs will be overwritten to either a random Local Long Code or Short Code to ensure delivery. All message content has to be whitelisted by local operators. It is highly advise to pre-register message content templates. Please make sure to always refer to our Acceptable Use Policy for Messaging.
5. Are there any SMS restrictions in Cambodia?
    > Based on the information provided, there are no SMS restrictions in Cambodia. Alphanumeric Sender IDs are supported and there are no restrictions with regards to content towards this destination. However, please make sure to always refer to Telnyx's Acceptable Use Policy for Messaging.
6. Is alphanumeric registration required in Poland?
    > In Poland, alphanumeric Sender IDs are supported and will be maintained, and no registration is required. However, it is recommended that Alpha Senders should be directly related to the message content. There are no restrictions with regards to content towards this destination. Please make sure to always refer to our Acceptable Use Policy for Messaging.

Other types of questions:

* Who are you?
    > I am an AI assistant designed to provide helpful customer service for Telnyx. My main focus is to assist with questions related to the Telnyx SMS Guidelines. How can I assist you today?
* What is the capital of Italy?
    > I'm sorry, but I am an AI assistant tuned to answer questions about the Telnyx SMS Guidelines. Unfortunately, I don't know the answer to your question. Please reformulate it or ask something different related to the Telnyx SMS Guidelines.
* What are the Telnyx SMS Guidelines?
    > The Telnyx SMS Guidelines are a set of rules and regulations that govern the use of SMS messaging services provided by Telnyx in different countries. These guidelines include information on supported alphanumeric sender IDs, registration requirements, restrictions on certain types of traffic such as gambling, and acceptable use policies. For more information on Alpha Sender ID registration, you can reach out to alpha_sender_id@telnyx.com.

Conversational memory:

* What is the country code for Italy?
    > The dial code for Italy is 39.
* And the MCC?
    > The MCC for Italy is 222.
* Is registration required?
    > Registration for what specifically? Please provide more context or specify which country or service you are referring to.
* Is registration in the same country required?
    > For Italy, no registration is required for Alphanumeric Sender IDs.
