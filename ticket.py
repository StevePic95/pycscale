import utils
import pandas as pd
import constants as const
from datetime import datetime

class TicketData:

    def __init__(self):
        # open file selection box with tkinter
        self.ODBC_filepath = utils.get_filepath_from_user("ODBC Import Excel File")
        self.OPR_filepath = utils.get_filepath_from_user("Operator Cash Report Excel File")

        # process dataframes
        df = utils.initialize_ticket_df(self.ODBC_filepath, print_updates=False)
        utils.transfer_data_to_empty_template(df, print_updates=False)
        df = utils.format_ticket_df(df, print_updates=False)
        cash_df_list = utils.create_opr_cash_dfs(self.OPR_filepath)

        # set processed dfs as attributes of TicketData object
        self.opr_df = cash_df_list[0]
        self.closed_short_tag_df = cash_df_list[1]
        self.open_short_tag_df = cash_df_list[2]
        self.main_df = utils.update_ticket_df(df, cash_df_list)

    def write_df_to_excel(self):
        now = datetime.now()
        new_excel_filepath = utils.get_directory_from_user() + "/pypcscale export " + now.strftime("%Y-%m-%d--%H-%M-%S") + ".xlsx"
        self.main_df.to_excel(new_excel_filepath, sheet_name="Sheet 1")




