## Project Description
The Fast-Food Ordering Chatbot is a conversational AI system that enables users to place food orders using natural language. It is built using Dialogflow ES for intent detection and entity extraction, with a FastAPI webhook backend deployed on Render and connected to a PostgreSQL database for persistent order storage. The frontend integrates Dialogflow Messenger and is deployed on Netlify.  
The system supports multi-turn conversations, session-wise order management, default quantity handling, item add/remove operations, bill generation, payment option selection (UPI and Cash on Delivery), order confirmation, and order tracking, demonstrating a fully deployed, production-style conversational application.

---

## Features of the Chatbot

#### Intent-Based Conversation Handling (Dialogflow ES)
The chatbot uses Dialogflow ES intents to classify user messages such as adding items, removing items, viewing the bill, selecting payment options, completing orders, and tracking orders. Each intent is mapped to a backend handler for structured processing.

#### Entity Extraction for Food Items, Quantities, and Payment Options
Dialogflow entities extract dynamic values like food items, quantities, order IDs, and payment modes, allowing natural phrases such as “add 2 pizza”, “remove samosa”, or “pay via UPI”.

#### Webhook Integration with FastAPI Backend
All detected intents and parameters are forwarded to a FastAPI webhook that handles validation, business logic, order state updates, and dynamic response generation.

#### Session-Wise Order State Management
Each user conversation is tied to a unique session ID, enabling consistent order tracking across multi-turn conversations without data loss.

#### Item Addition and Removal During Active Orders
Users can add or remove items at any stage of ordering, and the chatbot immediately reflects changes with an updated order summary.

#### Bill Generation and Payment Option Selection
Before finalizing the order, the chatbot calculates the total bill and prompts the user to choose a payment option such as **UPI** or **Cash on Delivery**, simulating a real checkout experience.

#### Order Completion and Confirmation
Once the payment option is selected, the order is saved in the database and confirmed with a unique order ID.

#### Persistent Order Storage and Tracking
Completed orders are stored in PostgreSQL, allowing users to later track order status using their order ID.

#### Web-Based Chat Interface Using Dialogflow Messenger
The chatbot is embedded in a web page using Dialogflow Messenger, providing a clean and interactive browser-based chat experience.

---

### Tech Stack Used

#### Dialogflow ES
Used for intent detection, entity extraction (food items, quantities, order IDs, payment options), and context management for multi-turn conversations.

#### FastAPI
Acts as the webhook backend to process Dialogflow requests, manage business logic, handle session-wise orders, calculate bills, and return responses.

#### PostgreSQL
Provides persistent storage for orders, order items, payment-related data, and order tracking status.

#### Dialogflow Messenger
Serves as the web-based chat interface embedded into the frontend.

#### Netlify
Hosts the static frontend containing the Dialogflow Messenger widget.

#### Render
Deploys the FastAPI backend and PostgreSQL database with HTTPS support required for Dialogflow webhooks.

---

### System Architecture
User (Browser)  
↓  
Static Frontend (Netlify)  
↓  
Dialogflow ES (Intent & Entity Detection)  
↓  
FastAPI Webhook (Render)  
↓  
PostgreSQL Database (Render)

---

### Folder Structure
MiraFastFood-Agent/
│
├── backend/
│ ├── main.py # FastAPI app & Dialogflow webhook handler
│ ├── db_helper.py # PostgreSQL database operations
│ ├── generic_helper.py # Utility/helper functions
│ └── requirements.txt # Backend dependencies
│
├── frontend/
│ └── index.html # Dialogflow Messenger-based chat UI
│
└── README.md # Project documentation


---

### Live Demo (works only when backend is live)
https://mirafastfood-site-grke.onrender.com/
