from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import db_helper
import generic_helper
from dialogflow_helper import detect_intent_and_params

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- GLOBALS ----------------
WEB_SESSION_ID = "web-session"
inprogress_orders = {}

# =========================================================
# CHAT API (Frontend / Postman / curl)
# =========================================================
@app.post("/chat")
async def chat(data: dict):
    # Safety check
    if "text" not in data or not data["text"]:
        return {"reply": "Please send a message."}

    text = data["text"]

    intent, parameters = detect_intent_and_params(text, WEB_SESSION_ID)

    intent_handler_dict = {
        "add.order": add_to_order,
        "remove.order": remove_from_order,
        "complete.order": complete_order,
        "order.track": track_order
    }

    handler = intent_handler_dict.get(intent)

    if not handler:
        return {"reply": "Sorry, I didn’t understand that."}

    # Call handler (returns JSONResponse)
    response = handler(parameters, WEB_SESSION_ID)

    # Extract fulfillmentText safely
    body = response.body.decode("utf-8")

    if "fulfillmentText" in body:
        reply = body.split("fulfillmentText\":\"")[1].split("\"")[0]
    else:
        reply = "Something went wrong."

    return {"reply": reply}


# =========================================================
# DIALOGFLOW WEBHOOK
# =========================================================
@app.post("/")
async def handle_request(request: Request):
    payload = await request.json()

    intent = payload["queryResult"]["intent"]["displayName"]
    parameters = payload["queryResult"]["parameters"]

    session = payload["session"]
    session_id = session.split("/")[-1]

    intent_handler_dict = {
        "add.order": add_to_order,
        "remove.order": remove_from_order,
        "complete.order": complete_order,
        "order.track": track_order
    }

    handler = intent_handler_dict.get(intent)

    if not handler:
        return JSONResponse(content={
            "fulfillmentText": "Sorry, I didn’t understand that."
        })

    return handler(parameters, session_id)


# =========================================================
# HELPERS
# =========================================================
def save_to_db(order: dict):
    order_id = db_helper.get_next_order_id()

    for food_item, quantity in order.items():
        rcode = db_helper.insert_order_item(food_item, quantity, order_id)
        if rcode == -1:
            return -1

    db_helper.insert_order_tracking(order_id, "in progress")
    return order_id


# =========================================================
# INTENT HANDLERS
# =========================================================
def add_to_order(parameters: dict, session_id: str):
    food_items = parameters.get("food_items") or []
    quantities = parameters.get("number") or []

    # Normalize to lists
    if not isinstance(food_items, list):
        food_items = [food_items]
    if not isinstance(quantities, list):
        quantities = [quantities]

    # Remove None values
    food_items = [f for f in food_items if f]
    quantities = [int(q) for q in quantities if q]

    if not food_items or not quantities or len(food_items) != len(quantities):
        return JSONResponse(content={
            "fulfillmentText": "I couldn't recognize the food item. Please try again."
        })

    new_items = dict(zip(food_items, quantities))

    if session_id not in inprogress_orders:
        inprogress_orders[session_id] = {}

    inprogress_orders[session_id].update(new_items)

    order_str = generic_helper.get_str_from_food_dict(
        inprogress_orders[session_id]
    )

    return JSONResponse(content={
        "fulfillmentText": f"So far you have: {order_str}. Do you need anything else?"
    })


def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText": "You don’t have an active order."
        })

    food_items = parameters.get("food_items") or []

    if not isinstance(food_items, list):
        food_items = [food_items]

    food_items = [f for f in food_items if f]

    current_order = inprogress_orders[session_id]

    removed = []
    not_found = []

    for item in food_items:
        if item in current_order:
            removed.append(item)
            del current_order[item]
        else:
            not_found.append(item)

    response = ""

    if removed:
        response += f"Removed {', '.join(removed)}. "

    if not_found:
        response += f"{', '.join(not_found)} were not in your order. "

    if not current_order:
        response += "Your order is empty."
    else:
        response += "Remaining: " + generic_helper.get_str_from_food_dict(current_order)

    return JSONResponse(content={
        "fulfillmentText": response.strip()
    })


def complete_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders or not inprogress_orders[session_id]:
        return JSONResponse(content={
            "fulfillmentText": "Your order is empty. Please add items first."
        })

    order = inprogress_orders[session_id]
    order_id = save_to_db(order)

    if order_id == -1:
        return JSONResponse(content={
            "fulfillmentText": "Failed to place order. Please try again."
        })

    total = db_helper.get_total_order_price(order_id)
    del inprogress_orders[session_id]

    return JSONResponse(content={
        "fulfillmentText": f"Order placed! ID {order_id}. Total ₹{total}."
    })


def track_order(parameters: dict, session_id: str):
    order_id = parameters.get("order_id")

    if not order_id:
        return JSONResponse(content={
            "fulfillmentText": "Please provide a valid order ID."
        })

    order_id = int(order_id)
    status = db_helper.get_order_status(order_id)

    if not status:
        return JSONResponse(content={
            "fulfillmentText": f"No order found with ID {order_id}."
        })

    return JSONResponse(content={
        "fulfillmentText": f"Order {order_id} is currently {status}."
    })
