class CreditCard:

    def __init__(self, customer, bank, acnt, limit):
        "Create a new credit card instance"
        self._customer = customer
        self._bank = bank
        self._acnt = acnt
        self._limit = limit
        self._balance  = 0
        
    def get_customer(self):
        "Return customer name"
        return self._customer
    
    def get_bank(self):
        "Return customer bank"
        return self._bank
    
    def get_acnt(self):
        "Return customer account"
        return self._acnt
    
    def get_limit(self):
        "Return customer limit"
        return self._limit
    
    def get_balance(self):
        "Return customer balance"
        return self._balance
    
    def charge(self, price):
        "Return true or false if there was a charge on the card"
        
        if price + self._balance > self._limit:
            return False
        else:
            self._balance += price
            return True
        
    def make_payment(self,amount):
        self._balance -= amount 
        return  self._balance
        
        
if __name__ == "__main__":
    wallet = []
    wallet.append(CreditCard('Jane Doe', ' Chase Bank', '5491 0032 8749 1111 9050', 2500))
    wallet.append(CreditCard('Charles Doe', ' CommerzBank', '2543 8584 1426 0878 9999', 5500))
    wallet.append(CreditCard('Jim Doe', ' Bank Of America', '7542 0983 1434 5453 8776', 10))
    
    
    for val in range(1,17):
        wallet[0].charge(val)
        print(f'{wallet[0].get_customer()}: Can be Charged {wallet[0].charge(val)}')
        wallet[1].charge(2*val)
        print(f'{wallet[1].get_customer()}: Can be Charged ${wallet[1].charge(2*val)}')
        wallet[2].charge(3*val)
        print(f'{wallet[2].get_customer()}: Can be Charged ${wallet[2].charge(3*val)}')
        
    for c in range(3):
        print(f'Customer: {wallet[c].get_customer()}')
        print(f'Bank: {wallet[c].get_bank()}')
        print(f'Account: {wallet[c].get_acnt()} ')
        print(f'Limit: {wallet[c].get_limit()}')
        print(f'Balance: {wallet[c].get_balance()}')
        
        while wallet[c].get_balance() > 100:
            wallet[c].make_payment(100)
            print(f'New Balance: {wallet[c].get_balance()}')
    
    
        
         