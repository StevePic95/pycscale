# %% Import necessary modules
import utils
import pandas as pd
import constants as const
import tkinter
from tkinter import filedialog

# %% Get file locations
ODBC_filepath = utils.get_filepath_from_user("ODBC File")
OPR_filepath = utils.get_filepath_from_user("OPR File")

# %% Create and show raw dataframe
pd.set_option("display.max_columns", None)
raw_df = pd.read_excel(ODBC_filepath)
raw_df.head()

# %% Drop junk columns from raw dataframe
junk_columns = const.ODBC_JUNK_COLUMNS
raw_df.drop(raw_df.columns[junk_columns], axis=1, inplace=True)
raw_df.head()

# %% Rename remaining columns
labeled_df = raw_df.rename(columns=const.ODBC_COLUMN_REINDEX_DICT)
labeled_df.head()

# %% Add new empty columns
import numpy as np
new_column_headers = const.ODBC_NEW_COLUMNS
for name in new_column_headers:
    labeled_df.loc[:, name] = np.nan
labeled_df.head()

# %% Set all "Split Load?" values to false for now
def rtn_false(x):
    return False
labeled_df[['Split Load?']] = labeled_df[['Split Load?']].apply(rtn_false)
labeled_df.head()

# %% Define masks for modifying split-load data
df = labeled_df
first_split_mask = (df['Ticket Number'].shift(-1) == df['Ticket Number']) & ~(df['Ticket Number'].shift(-2) == df['Ticket Number'])
second_split_mask = (df['Ticket Number'].shift(-2) == df['Ticket Number'])
top_rows_mask = (df['Ticket Number'].shift(1) == df['Ticket Number']) & ~(df['Ticket Number'].shift(-1) == df['Ticket Number'])
top_rows_w_second_split_mask = (df['Ticket Number'].shift(2) == df['Ticket Number']) & ~(df['Ticket Number'].shift(-1) == df['Ticket Number'])
keeper_rows_mask = (~(df['Ticket Number'].shift(-1) == df['Ticket Number']))

# %% mark split-load rows
df.loc[top_rows_mask, 'Split Load?'] = True

# %% Move first split data to corresponding blank values in first row with ticket number
df.loc[top_rows_mask, 'Percentage 2'] = df.loc[first_split_mask, 'Percentage 1'].values
df.loc[top_rows_mask, 'Origin 2']     = df.loc[first_split_mask, 'Origin Municipality 1'].values
df.loc[top_rows_mask, 'County 2']     = df.loc[first_split_mask, 'Origin County 1'].values
df.loc[top_rows_mask, 'Bill Code 2']  = df.loc[first_split_mask, 'Bill Code 1'].values

# %% Do the same for second splits
df.loc[top_rows_w_second_split_mask, 'Percentage 3'] = df.loc[second_split_mask, 'Percentage 1'].values
df.loc[top_rows_w_second_split_mask, 'Origin 3']     = df.loc[second_split_mask, 'Origin Municipality 1'].values
df.loc[top_rows_w_second_split_mask, 'County 3']     = df.loc[second_split_mask, 'Origin County 1'].values
df.loc[top_rows_w_second_split_mask, 'Bill Code 3']  = df.loc[second_split_mask, 'Bill Code 1'].values

# %% Delete the now redundant split rows
df = df.loc[keeper_rows_mask]
df.head()

# %% Make df from opr cash report
xl = pd.ExcelFile(OPR_filepath)
opr_df = xl.parse("Sheet1", header=2, names=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'])

# %% Remove junk columns
opr_df = opr_df.iloc[:,0:6]

# %% identify row borders between sections in df
closed_nips_start_row_index = opr_df[opr_df['A']=='CLOSED NOTICE OF INSUFFICIENT PAYMENTS'].index.item()
open_nips_start_row_index = opr_df[opr_df['A']=='OPEN NOTICE OF INSUFFICIENT PAYMENTS'].index.item()

# %% split into three separate dfs
main_df = opr_df.iloc[:closed_nips_start_row_index]
closed_nips_df = opr_df.iloc[closed_nips_start_row_index:open_nips_start_row_index]
open_nips_df = opr_df.iloc[open_nips_start_row_index:]

# %%
main_df.head()

# %%
closed_nips_df.head()

# %%
open_nips_df.head()

# %% Drop useless column from main_df
main_df.drop(main_df.columns[[3]], axis=1, inplace=True)
main_df.head()

# %% Fix column indexing on open_nips_df
open_nips_df = open_nips_df.reset_index(drop=True)
open_nips_df = open_nips_df.iloc[1:, :4]
open_nips_df = open_nips_df.reset_index(drop=True)
open_nips_df.columns = open_nips_df.iloc[0]
open_nips_df = open_nips_df.drop(0)
open_nips_df = open_nips_df.reset_index(drop=True)
open_nips_df.head()

# %% Fix column indexing on closed_nips_df
closed_nips_df = closed_nips_df.reset_index(drop=True)
new_columns = closed_nips_df.iloc[0][1:]
new_element = pd.Series(["Cash Paid"])
new_columns = new_columns.append(new_element)
closed_nips_df.columns = new_columns
closed_nips_df = closed_nips_df.reset_index(drop=True)
closed_nips_df = closed_nips_df.drop(0)
closed_nips_df.head()

# %% fix column indexing on main_df
main_df = main_df.rename(columns={"A": "Ticket Number", "B": "Date", "C": "Customer Name / Group", "E": "Pay Type", "F": "Cash Charge"})
main_df.head()

# %% Rename dfs
opr_df = main_df
main_df = df

# %% Show main_df formatting
main_df.head()

# %% Show opr_cash_df formatting
opr_df.head()

# %% Show open_nips_df formatting
open_nips_df.head()

# %% Show closed_nips_df formatting
closed_nips_df.head()

# %% Define masks for rows on main_df that will accept data from the other dfs
regular_cash_ticket_mask = main_df['Ticket Number'].isin(opr_df['Ticket Number'].values)
open_short_tag_cash_ticket_mask = main_df['Ticket Number'].isin(open_nips_df['Ticket'].values)
closed_short_tag_cash_ticket_mask = main_df['Ticket Number'].isin(closed_nips_df['Ticket'].values)

# %% Complete the "Cash?" column information
main_df.loc[:,'Cash?'] = False
main_df.loc[regular_cash_ticket_mask, 'Cash?'] = True


# %% Compute and fill cash charge/rounding adjustment data
def get_rounding_adjustment(pre_round_charge):
    pre_round_charge = str(pre_round_charge)
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

# %% Add cash charge data to empty column on main df
main_df.loc[regular_cash_ticket_mask,'Cash Charge'] = \
    main_df.loc[regular_cash_ticket_mask,"Unrounded Total Charge"] - \
        main_df.loc[regular_cash_ticket_mask,'Rounding Adjustment']

# %% See how main_df is doing so far
main_df.head()

# %% Add cash paid data to empty column on main df
main_df.loc[main_df['Cash?'] == True, 'Cash Charge'] = opr_df.loc[:,'Cash Charge']

# %% Check main_df again
main_df.head()

# %% Complete Short? Column on main_df
main_df.loc[:, "Short?"] = False
main_df.loc[open_short_tag_cash_ticket_mask,"Short?"] = True
main_df.loc[closed_short_tag_cash_ticket_mask,"Short?"] = True

# %% Complete Short Amount column on main_df
short_mask = main_df["Short?"] == True
main_df.loc[short_mask,"Short Amount"] = open_nips_df["Amount"]

# %% Complete Pay Type column on main_df
main_df.loc[regular_cash_ticket_mask,"Pay Type"] = opr_df['Pay Type']

# %% Complete Short Paid? column on main_df
main_df.loc[closed_short_tag_cash_ticket_mask,"Short Paid?"] = True
main_df.loc[open_short_tag_cash_ticket_mask,"Short Paid?"] = False

# %% Complete Short Paid Date column on main_df
main_df.loc[closed_short_tag_cash_ticket_mask,"Short Paid Date"] = closed_nips_df["Close Date"]

# %% Check main_df
main_df.head()

# %% Send main_df to excel file
main_df.to_csv("Data\\test.csv")

