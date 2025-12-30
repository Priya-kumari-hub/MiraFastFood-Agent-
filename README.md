## Project description
The Fast-Food Ordering Chatbot is a conversational AI system that enables users to place food orders using natural language. It is built using Dialogflow ES for intent detection and entity extraction, with a FastAPI webhook backend deployed on Render, connected to a PostgreSQL database for persistent order storage. The frontend integrates Dialogflow Messenger and is deployed on Netlify. The system supports multi-turn conversations, session-wise order management, default quantity handling, item add/remove operations, order confirmation, and order tracking, demonstrating a fully deployed, production-style conversational application.

### Features of the Chatbot
#### Intent-Based Conversation Handling (Dialogflow ES)
The chatbot uses Dialogflow ES intents to classify user messages such as adding items, removing items, completing orders, and tracking orders. Each intent is mapped to a specific backend function, enabling accurate and structured handling of user requests.

#### Entity Extraction for Food Items and Quantities
Dialogflow entities are used to extract dynamic values like food items and quantities from user input. System entities such as numbers and custom food item entities allow the chatbot to understand phrases like “add 2 pizza” or “remove samosa” without rigid command formats.

#### Webhook Integration with FastAPI Backend
Detected intents and extracted parameters are sent to a FastAPI webhook. The backend processes business logic, validates parameters, and generates appropriate responses, ensuring a clean separation between NLP and application logic.

#### Session-Wise Order State Management
Each conversation is associated with a unique session ID, enabling the chatbot to track the order state across multiple interactions. This ensures consistent behavior even in long, multi-turn conversations.

#### Item Addition and Removal During Active Orders
Users can dynamically add or remove items at any point during the conversation. The chatbot immediately reflects these changes and provides an updated order summary after each interaction.

#### Order Completion and Confirmation
When the user indicates they are done (e.g., by saying “no”), the chatbot finalizes the order, stores it in the database, and confirms the order with a unique order ID.

#### Persistent Order Storage and Tracking
Completed orders are stored in a PostgreSQL database, enabling order tracking functionality. Users can later query the chatbot using an order ID to check the status of their order.

#### Web-Based Chat Interface Using Dialogflow Messenger
The chatbot is integrated into a web interface using Dialogflow Messenger, allowing users to interact with the system directly from a browser in a user-friendly chat format.
