from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import db_helper
import generic_helper


app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        "order.track": track_order,
        "payment.option": bill_payment,
        "cash.payment" : cash_payment,
        "upi.payment" : upi_payment
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
inprogress_orders = {}
def add_to_order(parameters: dict, session_id: str):
    food_items = parameters["food_items"]
    quantities = parameters["number"]

    

    # default quantity = 1
    if not quantities:
        quantities = [1] * len(food_items)
    else:
        quantities = [int(q) if q else 1 for q in quantities]

    # align lengths
    if len(quantities) < len(food_items):
        quantities += [1] * (len(food_items) - len(quantities))

    if not food_items:
        return JSONResponse(content={
            "fulfillmentText": "I couldn't recognize the food item. Please try again."
        })

    if session_id not in inprogress_orders:
        inprogress_orders[session_id] = {}

    # accumulate quantities
    for item, qty in zip(food_items, quantities):
        inprogress_orders[session_id][item] = (
            inprogress_orders[session_id].get(item, 0) + qty
        )

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

    removed, not_found = [], []

    for item in food_items:
        if item in current_order:
            removed.append(item)
            del current_order[item]
        else:
            not_found.append(item)

    msg = ""
    if removed:
        msg += f"Removed {', '.join(removed)}. "
    if not_found:
        msg += f"{', '.join(not_found)} were not in your order. "

    if not current_order:
        msg += "Your order is empty, please add something."
    else:
        msg += "Remaining items: " + generic_helper.get_str_from_food_dict(current_order)

    return JSONResponse(content={"fulfillmentText": msg.strip()})


def bill_payment(parameters: dict, session_id: str):
    if session_id not in inprogress_orders or not inprogress_orders[session_id]:
        return JSONResponse(content={
            "fulfillmentText": "Your order is empty. Please add items first."
        })
    order = inprogress_orders[session_id]
    total = db_helper.get_total_order_price(order_id)

    return JSONResponse(content={ 
        "fulfillmentText": f"Great! your total bill is ₹{total}, please select the payment option 1.UPI(Google Pay, Phone Pay, Paytm, Paypal, NaviUPI, BHIM, Razorpay, Bharat pay, Amazon pay) 2.Cash on devilery."
    })


def cash_payment(parameters: dict, session_id: str):
    order = inprogress_orders[session_id]
    order_id = save_to_db(order) 
  
    if order_id == -1:
        return JSONResponse(content={
            "fulfillmentText": "Failed to place order. Please try again."
        })

    del inprogress_orders[session_id]
    return JSONResponse(content={ 
        "fulfillmentText": f"Awesome! your order has been placed, order ID #{order_id}"
    })
def upi_payment(parameters: dict, session_id: str):  
    order = inprogress_orders[session_id]
    order_id = save_to_db(order) 
  
    if order_id == -1:
        return JSONResponse(content={
            "fulfillmentText": "Failed to place order. Please try again."
        })

    del inprogress_orders[session_id]
    return JSONResponse(content={ 
        "fulfillmentText": f"Awesome! your order has been placed,your order ID #{order_id}."
    })
    

    
def track_order(parameters: dict, session_id: str):
    # Dialogflow sends order id as "number"
    order_id =  parameters.get("number")

    status = db_helper.get_order_status(order_id)

    if not status:
        return JSONResponse(content={
            "fulfillmentText": f"No order found with ID {order_id}."
        })

    return JSONResponse(content={
        "fulfillmentText": f"Order {order_id} is currently {status}."
    })












