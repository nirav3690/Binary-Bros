class CreditCardGateway:

    def initiate_charge(self, rupees: float, card_holder: str) -> str:
        print(f"  [CreditCardGateway] Charging ₹{rupees} to: {card_holder}")
        return f"TXN_CC_{id(self)}"

    def reverse_charge(self, txn_ref: str) -> bool:
        print(f"  [CreditCardGateway] Reversing: {txn_ref}")
        return True