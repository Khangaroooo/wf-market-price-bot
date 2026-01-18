import json

class Order:
    def __init__(self, raw_order):
        self.id = raw_order.get("id")
        self.type = raw_order.get("type")
        self.platinum = raw_order.get("platinum")
        self.item_id = raw_order.get("itemId")

    def toString(self):
        return json.dumps(self.__dict__)