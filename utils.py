import tkinter
from tkinter import filedialog
import pandas as pd
from pip import main
import constants as const
import re
import numpy as np
from datetime import datetime
import openpyxl

def get_filepath_from_user(file_type):
    """
    Opens a dialogue box for user to choose CSV report files to convert.
    Note: the file_type parameter should be passed the name of the report
    you want to get from the user. The argument will just be used to give
    the dialog window a descriptive title.
    """
    root = tkinter.Tk()
    root.withdraw() # hide tkinter gui
    file_path = filedialog.askopenfilename(title="Select the " + file_type + " file.")

    return file_path


def get_directory_from_user():
    """Opens a dialog box for user to select a directory to export files
    from the module."""
    root = tkinter.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Choose a folder to export the Excel file to.")

    return directory


def initialize_ticket_df(ticketODBC, print_updates=True):
    """
    Uses pandas to read the ODBC_Imports excel file and create a dataframe
    ready to be formatted
    """
    if print_updates:
        print("Creating new ticket dataframe. \
            NOTE: Returned dataframe will still need to be \
                formatted and updated with cash data.")
    df = pd.read_excel(ticketODBC)

    return df


def print_col_names(df): ################
    list = df.columns.tolist()
    i = 0
    for name in list:
        print(str(i) + ": " + name)
        i += 1

def transfer_data_to_empty_template(raw_df, print_updates=False):

    # Create new empty dataframe with column names defined from constants.py
    column_names = const.ODBC_UPDATED_COLUMN_NAMES
    new_df = pd.DataFrame(columns=column_names)

    old_columns = const.ODBC_ORIGINAL_COLUMN_NAMES
    new_columns = const.ODBC_UPDATED_COLUMN_NAMES

    for old_column, new_column in old_columns, new_columns[:len(old_columns) + 1]:
        new_df[[new_column]] = raw_df[[old_column]]
    
    


def format_ticket_df(df, print_updates=True): # Possibly replacing with a function that builds an empty df and populates info from the raw df
    """
    Formats the pandas dataframe by removing junk columns, adding columns
    for ticket attributes not included in the original ODBC import, and combining
    split-load tickets occupying multiple rows. Does NOT complete the ticket data.
    """
    junk_columns = const.ODBC_JUNK_COLUMNS
    new_column_headers = const.ODBC_NEW_COLUMNS

    # Remove junk columns
    df.drop(df.columns[junk_columns], axis=1, inplace=True)
    if print_updates:
        print("Dropped junk columns from dataframe")

    # Rename old columns
    df = df.reindex(columns=const.ODBC_UPDATED_COLUMN_NAMES, axis=1)
    if print_updates:
        print("Renamed old columns.")

    # Add and fill new columns with NaN values
    for name in new_column_headers:
        df.loc[:, name] = np.nan
    if print_updates:
        print("Added and filled new columns with NaN values")

    # Set split load? to False for all rows for now
    def rtn_false(x):
        return False
    df[['Split Load?']] = df[['Split Load?']].apply(rtn_false)
    if print_updates:
        print("Temporarily marked all tickets \"Split Load?\"=False")

    # Identify split load tickets by finding rows with same ticket number as the row above
    # (or two rows above for triple-splits which are the max allowed).
    # Keep in mind: boolean indexing in pandas returns a copy of the dataframe, not a view.
    # We instead save the criteria for the different types of rows we want to alter
    # as masks for direct access to the original df.
    first_split_mask = (df['Ticket Number'].shift(-1) == df['Ticket Number']) & ~(df['Ticket Number'].shift(-2) == df['Ticket Number'])
    second_split_mask = (df['Ticket Number'].shift(-2) == df['Ticket Number'])
    top_rows_mask = (df['Ticket Number'].shift(1) == df['Ticket Number']) & ~(df['Ticket Number'].shift(-1) == df['Ticket Number'])
    top_rows_w_second_split_mask = (df['Ticket Number'].shift(2) == df['Ticket Number']) & ~(df['Ticket Number'].shift(-1) == df['Ticket Number'])
    keeper_rows_mask = (~(df['Ticket Number'].shift(-1) == df['Ticket Number']))
    if print_updates:
        print("Defined masks for modifying split-load data")

    # Mark split load rows
    df.loc[top_rows_mask, 'Split Load?'] = True
    if print_updates:
        print('Marked \"Split Load?\" True for split-load tickets')

    # Move first split data to corresponding blank values in first row with ticket number
    df.loc[top_rows_mask, 'Percentage 2'] = df.loc[first_split_mask, 'Percentage 1'].values
    df.loc[top_rows_mask, 'Origin 2']     = df.loc[first_split_mask, 'Origin Municipality 1'].values
    df.loc[top_rows_mask, 'County 2']     = df.loc[first_split_mask, 'Origin County 1'].values
    df.loc[top_rows_mask, 'Bill Code 2']  = df.loc[first_split_mask, 'Bill Code 1'].values
    if print_updates:
        print("Moved ticket data from first split rows to top rows")

    # Do the same for second splits
    df.loc[top_rows_w_second_split_mask, 'Percentage 3'] = df.loc[second_split_mask, 'Percentage 1'].values
    df.loc[top_rows_w_second_split_mask, 'Origin 3']     = df.loc[second_split_mask, 'Origin Municipality 1'].values
    df.loc[top_rows_w_second_split_mask, 'County 3']     = df.loc[second_split_mask, 'Origin County 1'].values
    df.loc[top_rows_w_second_split_mask, 'Bill Code 3']  = df.loc[second_split_mask, 'Bill Code 1'].values
    if print_updates:
        print("Moved ticket data from second split rows to top rows")

    # Delete the now redundant split rows by keeping only rows without the same ticket number above them (see keeper_rows_mask definition ^)
    df = df.loc[keeper_rows_mask]
    if print_updates:
        print("Removed first and second split rows")

    ###########TEMPORARY TEST################
    now = datetime.now()
    new_excel_filepath = get_directory_from_user() + "/pypcscale export " + now.strftime("%Y-%m-%d--%H-%M-%S") + ".xlsx"
    df.to_excel(new_excel_filepath, sheet_name="Sheet 1", engine='openpyxl')

    return df


def create_opr_cash_dfs(path_to_excel_file):
    """
    Returns a list of formatted dfs from Operator Cash excel file which can be used
    to fill the gaps in the formatted ticket df.
    """
    xl = pd.ExcelFile(path_to_excel_file)
    df = xl.parse("Sheet1", header=2, names=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'])

    # remove junk columns
    df = df.iloc[:,0:6]

    # identify row borders between sections in df
    closed_nips_start_row_index = df[df['A']=='CLOSED NOTICE OF INSUFFICIENT PAYMENTS'].index.item()
    open_nips_start_row_index = df[df['A']=='OPEN NOTICE OF INSUFFICIENT PAYMENTS'].index.item()

    # split df into three separate dfs for each section of the original excel file
    main_df = df.iloc[:closed_nips_start_row_index]
    closed_nips_df = df.iloc[closed_nips_start_row_index:open_nips_start_row_index]
    open_nips_df = df.iloc[open_nips_start_row_index:]

    # remove junk rows from each of the new dfs by keeping only rows that reference a ticket number
    # (regex can be modified in constants.py for any companies with a different ticket number system)
    main_df = main_df.loc[main_df['A'].apply(lambda x: True if re.fullmatch(const.TICKET_NUM_REGEX, str(x)) else False),:]
    closed_nips_df = closed_nips_df.loc[closed_nips_df['B'].apply(lambda x: True if re.fullmatch(const.TICKET_NUM_REGEX, str(x)) else False),:]
    open_nips_df = open_nips_df.loc[open_nips_df['A'].apply(lambda x: True if re.fullmatch(const.TICKET_NUM_REGEX, str(x)) else False),:]

    # reset indexes for each new df since they still have their index from the original df
    # (drop is true to prevent the old index being added as a new column)
    main_df = main_df.reset_index(drop=True)
    closed_nips_df = closed_nips_df.reset_index(drop=True)
    open_nips_df = open_nips_df.reset_index(drop=True)

    # rename columns to finish cleaning the data
    main_df.rename(columns={'A': 'Ticket Number', 'B': 'Date', 'C': 'Customer', 'D': 'I', 'E': 'Pay Method', 'F': 'Cash Paid'}, inplace=True)
    closed_nips_df.rename(columns={'A': 'Operator', 'B': 'Ticket Number', 'C': 'Date Closed', 'D': 'Time Closed', 'E': 'Workstation', 'F': 'Cash Paid'}, inplace=True)
    open_nips_df = open_nips_df.iloc[:,0:4] # Remove blank columns
    open_nips_df.rename(columns={'A': 'Ticket Number', 'B': 'License Plate or DL Number', 'C': 'Date Opened', 'D': 'Short Amount'}, inplace=True)

    # Place finished dfs into a list that will be returned
    df_list = [main_df, closed_nips_df, open_nips_df]

    return df_list


def update_ticket_df(df, cash_df_list):
    """
    Updates the formatted pandas dataframe using info from Operator Cash Report
    """
    # Name list elements
    main_df = df
    opr_df = cash_df_list[0]
    closed_nips_df = cash_df_list[1]
    open_nips_df = cash_df_list[2]

    # Rename 

    # define masks for rows on main_df that will accept data from the other dfs
    regular_cash_ticket_mask = main_df['Ticket Number'].isin(opr_df['Ticket Number'].values)
    open_short_tag_cash_ticket_mask = main_df['Ticket Number'].isin(open_nips_df['Ticket Number'].values)
    closed_short_tag_cash_ticket_mask = main_df['Ticket Number'].isin(closed_nips_df['Ticket Number'].values)
    
    # Complete the "Cash?" column information
    main_df.loc[:,'Cash?'] = False
    main_df.loc[regular_cash_ticket_mask, 'Cash?'] = True 
    
    # Compute and fill cash charge/rounding adjustment data
    def get_rounding_adjustment(pre_round_charge):
        if "." not in pre_round_charge:
            return 0.00
        else:
            cents = pre_round_charge.split(".")[-1]
            if len(cents) == 1:
                cents = int(cents) * 10
            else:
                cents = int(cents)
        if cents < 25:
            return round(cents / 100, 2)
        elif cents < 50:
            return round((cents - 25) / 100, 2)
        elif cents < 75:
            return round((cents - 50) / 100, 2)
        elif cents < 100:
            return round((cents - 75) / 100, 2)
    main_df.loc[regular_cash_ticket_mask, 'Rounding Adjustment'] = \
        main_df.loc[regular_cash_ticket_mask, "Unrounded Total Charge"]\
            .apply(get_rounding_adjustment)
    
    # Add cash charge data to empty column on main df
    main_df.loc[regular_cash_ticket_mask,'Cash Charge'] = \
        main_df.loc[regular_cash_ticket_mask,"Unrounded Total Charge"] - \
            main_df.loc[regular_cash_ticket_mask,'Rounding Adjustment']
    
    # Add cash paid data to empty column on main df
    main_df.loc[regular_cash_ticket_mask,'Cash Paid'] = np.nan
    main_df.loc[main_df['Cash?'] == True, 'Cash Paid'] = opr_df.loc[:,'Cash Paid']

    # Complete Short? Column on main_df
    main_df.loc[:, "Short?"] = False
    main_df.loc[open_short_tag_cash_ticket_mask,"Short?"] = True
    main_df.loc[closed_short_tag_cash_ticket_mask,"Short?"] = True

    # Complete Short Amount column on main_df
    short_mask = main_df["Short?"] == True
    main_df.loc[short_mask,"Short Amount"] = open_nips_df["Amount"]

    # Complete Pay Type column on main_df
    main_df.loc[regular_cash_ticket_mask,"Pay Type"] = opr_df['Pay Type']

    # Complete Short Paid? column on main_df
    main_df.loc[closed_short_tag_cash_ticket_mask,"Short Paid?"] = True
    main_df.loc[open_short_tag_cash_ticket_mask,"Short Paid?"] = False

    # Complete Short Paid Date column on main_df
    main_df.loc[closed_short_tag_cash_ticket_mask,"Short Paid Date"] = closed_nips_df["Close Date"]

    return main_df


