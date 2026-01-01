Project description

The Fast-Food Ordering Chatbot is a conversational AI system that enables users to place food orders using natural language. It is built using Dialogflow ES for intent detection and entity extraction, with a FastAPI webhook backend deployed on Render, connected to a PostgreSQL database for persistent order storage. The frontend integrates Dialogflow Messenger and is deployed on Netlify. The system supports multi-turn conversations, session-wise order management, default quantity handling, item add/remove operations, bill generation, payment option selection (UPI and Cash on Delivery), order confirmation, and order tracking, demonstrating a fully deployed, production-style conversational application.

Features of the Chatbot
Intent-Based Conversation Handling (Dialogflow ES)

The chatbot uses Dialogflow ES intents to classify user messages such as adding items, removing items, viewing the bill, selecting payment options, completing orders, and tracking orders. Each intent is mapped to a specific backend function, enabling accurate and structured handling of user requests.

Entity Extraction for Food Items, Quantities, and Payment Options

Dialogflow entities are used to extract dynamic values like food items, quantities, order IDs, and payment modes from user input. This allows the chatbot to understand phrases like “add 2 pizza”, “remove samosa”, or “pay using UPI” without rigid command formats.

Webhook Integration with FastAPI Backend

Detected intents and extracted parameters are sent to a FastAPI webhook. The backend processes business logic, validates parameters, maintains order state, calculates the total bill, and generates appropriate responses, ensuring a clean separation between NLP and application logic.

Session-Wise Order State Management

Each conversation is associated with a unique session ID, enabling the chatbot to track the order state across multiple interactions. This ensures consistent behavior even in long, multi-turn conversations.

Item Addition and Removal During Active Orders

Users can dynamically add or remove items at any point during the conversation. The chatbot immediately reflects these changes and provides an updated order summary after each interaction.

Bill Generation and Payment Option Selection

Before order completion, the chatbot calculates the total bill for the active order and prompts the user to choose a payment method such as UPI or Cash on Delivery, simulating a real-world checkout experience.

Order Completion and Confirmation

When the user confirms the payment option, the chatbot finalizes the order, stores it in the database, and confirms the order with a unique order ID.

Persistent Order Storage and Tracking

Completed orders are stored in a PostgreSQL database, enabling order tracking functionality. Users can later query the chatbot using an order ID to check the status of their order.

Web-Based Chat Interface Using Dialogflow Messenger

The chatbot is integrated into a web interface using Dialogflow Messenger, allowing users to interact with the system directly from a browser in a user-friendly chat format.

Tech Stack used
Dialogflow ES--

Used for intent detection, entity extraction (food items, quantities, order IDs, payment options), and context management to enable natural language, multi-turn conversations.

FastAPI-

Serves as the webhook backend to process Dialogflow requests, handle business logic, manage session-wise orders, calculate bills, and generate chatbot responses.

PostgreSQL-

Provides persistent storage for completed orders, payment-related order data, and order tracking status, ensuring reliability and data consistency.

Dialogflow Messenger-

Acts as the web-based chat interface that embeds the chatbot into a browser-accessible frontend.

Netlify-

Hosts the static frontend containing the Dialogflow Messenger, ensurin
