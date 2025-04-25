
from credit_card import CreditCard

class PredatoryCreditCard(CreditCard):
    
    OVERLIMIT_FEE = 5
    
    def __init__(self, customer, bank, acnt, limit, apr):
        
        super().__init__(customer,bank,acnt,limit)
        self._apr = apr
        
        
    def charge(self, price):
        """
        Charge given price to the card, assuming sufficient credit limit
        
        Return True if charge was processed.
        Return False and assess $5 fee if charge is denied.
        """
        
        
        success = super().charge(price)
        
        if not success:         # call inherited method 
            self._balance += PredatoryCreditCard.OVERLIMIT_FEE  # assess penalty
        return success          # caller expects return value
    

    def process_mont(self):
        """Assess monthly interest on outstanding balance"""
        if self._balance > 0 :
            # if positve balance, convert APR to monthly multiplicative factor
            monthly_factor = pow(1 + self._apr, 1/12)
            self._balance += monthly_factor
            
             
            