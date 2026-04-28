class CreditCardGateway:
    def initiate_charge(self, rupees, card_holder):
        print(f"  [CreditCardGateway] Charging ₹{rupees} to: {card_holder}")
        return f"TXN_CC_{id(self)}"
    def reverse_charge(self, txn_ref):
        print(f"  [CreditCardGateway] Reversing: {txn_ref}")
        return True