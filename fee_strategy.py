class FeeStrategy:
    def calculate_fee(self):
        raise NotImplementedError

class RegularFee(FeeStrategy):
    def calculate_fee(self):
        return 100  # Example: flat fee

class ElectricFee(FeeStrategy):
    def calculate_fee(self):
        return 50  # Discounted EV fee
