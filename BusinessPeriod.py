class BusinessPeriod:
    """
    Container for most of the other classes in this module with 
    """
    def __init__(self, force_update=True):
        if force_update:
            self.ticketData = TicketData