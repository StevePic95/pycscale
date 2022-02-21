import pandas as pd
from utils import format_ticket_df
from utils import get_filepath_from_user, create_opr_cash_dfs, create_ticket_df, format_ticket_df, update_ticket_df

class TicketData:

    def __init__(self):
        # open file selection box with tkinter
        self.ODBC_filepath = get_filepath_from_user("ODBC Import Excel File")
        self.OPR_filepath = get_filepath_from_user("Operator Cash Report Excel File")

        # process dataframes
        df = create_ticket_df(self.ODBC_filepath)
        df = format_ticket_df(df)
        cash_df_list = create_opr_cash_dfs(self.OPR_filepath)

        self.opr_df = cash_df_list[0]
        self.closed_short_tag_df = cash_df_list[1]
        self.open_short_tag_df = cash_df_list[2]
        self.main_df = update_ticket_df(df, cash_df_list)


class BusinessPeriod:
    """
    Container for most of the other classes in this module with 
    """
    def __init__(self, force_update=True):
        if force_update:
            self.ticketData = TicketData