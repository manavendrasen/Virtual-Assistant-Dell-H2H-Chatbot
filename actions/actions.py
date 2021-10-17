from typing import Any, Text, Dict, List

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
class FetchOrderDetails(Action):
    def name(self) -> Text:
        return "action_fetch_order"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        orderNumber = tracker.get_slot("order_number")
        
        if not orderNumber:
            msg = "Please Enter order number"
            dispatcher.utter_message(text=msg)
            return []
        
        try:
            result = requests.get(f"https://nameless-gorge-89729.herokuapp.com/orders/{orderNumber}").json()
            print(result)

            dispatcher.utter_message(
            image=result['imageUrl'],
            text=f"Order ID: {orderNumber} \nProduct Name: {result['productname']}"
            )

            # if error
            if "issueId" in result.keys():
                dispatcher.utter_message(
                    text=f"Order in ON-HOLD, Issue: {result['errorName'].capitalize()} is invalid"
                )
                return [SlotSet("hasError", True), SlotSet("issueId", result["issueId"]),SlotSet("errorID", result["errorId"]), SlotSet("errorName", result["errorName"]) ]
            
            else:
                dispatcher.utter_message(
                    text=f"Order was SUCCESSFUL"
                )
                return [SlotSet("hasError", False)]
                
            
        except:
            dispatcher.utter_message(
                    text="There was some issue fetching data. Make Sure you have entered the correct Order ID\nTry again later.\n"
                ) 

        return []

class UpdateOrderDetails(Action):
    def name(self) -> Text:
        return "action_update_order"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        orderNumber = tracker.get_slot("order_number")
        issueId = tracker.get_slot("issueId")
        errorID = tracker.get_slot("errorID")
        errorName = tracker.get_slot("errorName")

        if(errorID == 100):
            email = tracker.get_slot("email")
            data={"orderEmail": email}

        elif(errorID == 101):
            zip_code = tracker.get_slot("zip_code")
            data={"zipCode": int(zip_code)}

        elif(errorID == 102):
            msg = "The email has been found in the fraud list."
            dispatcher.utter_message(text=msg)
            return []

        if not orderNumber:
            msg = "Please Enter Order ID"
            dispatcher.utter_message(text=msg)
            return []

        try: 
            result = requests.post(f"https://nameless-gorge-89729.herokuapp.com/orders/{orderNumber}/{issueId}/{errorID}", json=data)
            if(errorID == 102):
                dispatcher.utter_message(
                text=f"Email in Fraud List."
                ) 
            else: 
                dispatcher.utter_message(
                    text=f"{errorName.capitalize()} Updated Successfully"
                )   
            
        except: 
            dispatcher.utter_message(
                text=f"{errorName.capitalize()} Update Failed, Try again later."
            ) 
        return []

class FetchOrderDetailsForCustomers(Action):
    def name(self) -> Text:
        return "action_fetch_order_for_customer"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        orderNumber = tracker.get_slot("order_number")
        
        if not orderNumber:
            msg = "Please Enter order number"
            dispatcher.utter_message(text=msg)
            return []
        
        try:
            result = requests.get(f"https://nameless-gorge-89729.herokuapp.com/orders/{orderNumber}").json()
            print(result)
            
            productName = result['productname']
            orderStatus = result['orderStatus']
            productDesc = result['productDesc']
            imageUrl = result['imageUrl']
            quantity = result['quantity']
            orderDate = result['orderDate']
            price = result['price']

            dispatcher.utter_message(
            image=imageUrl,
            text=f"*Order ID:* {orderNumber} \n------- \n*Product Name:* {productName} \n*Quantity:* {quantity}\n*Product Description:* {productDesc}\n*Ordered on:* {orderDate} \n*Total Price*: {price*quantity} \n*Order Status: {orderStatus}*"
            )

            # if error
            if "issueId" in result.keys():
                errorName = result['errorName']
                print(f"The Order has an issue - {errorName.capitalize()} is invalid. \nA Dell representative will contact you to resolve this issue.")
                dispatcher.utter_message(
                    text=f"The Order has some issues, Issue: {errorName.capitalize()} is invalid, \nA Dell representative will contact you to resolve this issue."
                )

        except:
            dispatcher.utter_message(
                text="There was some issue fetching data. Make Sure you have entered the correct Order ID\nTry again later.\n"
            )

        return []

    
class IsUserUsingWhatsapp(Action):
    def name(self) -> Text:
        return "action_is_user_using_whatsapp"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.get_latest_input_channel())
        if(tracker.get_latest_input_channel() == "twilio"):
            return [SlotSet("isOnWhatsapp", True)]
        else:
            return [SlotSet("isOnWhatsapp", False)]
    