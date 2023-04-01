#class for pricing module
class pricing:

    def __init__(self, location, history, gal_requested):
        self.location = location
        self.history = history
        self.gal_requested = gal_requested

            
        if self.location == 'TX':
            self.location_factor = 0.02
        else:
            self.location_factor = 0.04

        if self.history == True:
            self.rate_history_factor = 0.01
        else :
            self.rate_history_factor = 0

        if self.gal_requested > 1000:
            self.gallons_requested_factor = 0.02
        else:
            self.gallons_requested_factor = 0.03
        
        self.company_profit = 0.1
        self.curr_gas_price = 1.50

    def get_suggested_price(self):

        margin = self.curr_gas_price * (self.location_factor - self.rate_history_factor + self.gallons_requested_factor + self.company_profit)
        suggested_price = self.curr_gas_price + margin

        return suggested_price
    
    def total_amount(self):
        return self.gal_requested * self.get_suggested_price()
