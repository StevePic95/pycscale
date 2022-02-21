# Documentation for the pypcscale Module
---
### How to Generate the necessary CSV Files from PC Scale

#### TicketTable Objects
* MAIN SOURCE OF DATA: ODBC_Imports data-only Excel file
 * Formatting options:

* AUXILLIARY DATA SOURCES:
 * Operator Cash Report data-only Excel file


 ### Standard Dataframe Column Names
 #### main_df
* 0: Index
* 1: GH1_INBOUND_TICKET -> Ticket Number (int)
* 2: GH1_CustAdd -> Customer Address (string)
* 3: GH1_INBOUND_CUSTOMER -> Customer (string)
* 4: GH1_CarrAdd -> Carrier Address (string)
* 5: GH1_INBOUND_DATE -> Weigh-in Date (datetime.date object)
* 6: GH1_INBOUND_TIME_IN -> Weigh-in Time (datetime.time object)
* 7: GH1_INBOUND_IN_OPERATOR -> Weigh-in Operator (string)
* 8: GH1_INBOUND_TIME_OUT -> Weigh-out Time (datetime.time object)
* 9: GH1_INBOUND_OUT_OPERATOR -> Weigh-out Operator (string)
* 10: GH1_ShowGross -> Gross Weight lbs (int)
* 11: GH1_Tare -> Tare Weight lbs (int)
* 12: GH1_Net -> Net Weight lbs (int)
* 13: GH1_GTons -> Gross Weight Tons (float)
* 14: GH1_TTons -> Tare Weight Tons (float)
* 15: GH1_NTons -> Net Weight Tons (float)
* 16: GH1_INBOUND_TRUCK -> Vehicle Number (string)
* 17: GH1_Type -> Vehicle Type (string)
* 18: GH1_INBOUND_LICENSE -> License Plate (string)
* 19: GH1_INBOUND_TRAILER -> Trailer Number (string)
* 20: GH1_INBOUND_CUYDS -> Trailer Volume Yards (float)
* 21: GH2_Sum_(_IPDETAIL_QUANTITY_,__IPDETAIL_WASTE_) -> Sum Weight Tons (float)
* 22: GH2_IPDETAIL_WASTE -> Bill Code 1 (string)
* 23: GH2_WasteLine -> Bill Code Description 1 (string)
* 24: GH2_Units -> Charge Units 1 (string)
* 25: GH2_Rate -> Charge Rate 1 (float)
* 26: GH2_Sum_(_IPDETAIL_PRETAX_,__IPDETAIL_WASTE_) -> Unrounded Total Charge (float)
* 27: DE_IPDETAIL_ORIGIN -> Origin Code 1 (string)
* 28: DE_ORIGIN_NAME -> Origin Municipality 1 (string)
* 29: DE_COUNTY_NAME -> Origin County 1 (string)
* 30: DE_IPDETAIL_PCT -> Percentage 1 (float)
* 31: PF_DEPInfo -> Carrier DEP Number (string)
* 32: PF_Comments -> Ticket Comments (string)
* 33: PF_SumTaxes -> Tax Sum (float)
* 34: PF_TotalAmount -> Ticket Revenue (float)
* 35: Cash? (bool)
* 36: Rounding Adjustment (float)
* 37: Cash Charge (float)
* 38: Cash Paid (float)
* 39: Short? (bool)
* 40: Short Amount (float)
* 41: Pay Type (string)
* 42: Short Paid? (bool)
* 43: Short Paid Date (datetime.date object)
* 44: Updated? (bool)
* 45: Last Update (datetime.datetime object)
* 46: Split Load? (bool)
* 47: Percentage 2 (float)
* 48: Origin 2 (string)
* 49: County 2 (string)
* 50: Bill Code 2 (string)
* 51: Percentage 3 (float)
* 52: Origin 3 (string)
* 53: County 3 (string)
* 54: Bill Code 3 (string)
* 55: 
* 56: 
* 57: 
* 58: 
* 59: 
* 60: 
* 61: 
* 62: 
* 63: 
* 64: 
* 65: 
* 66: 
* 67: 
* 68: 
* 69: 
* 70: 
 #### opr_cash_df
* 0: Ticket Number
* 1: Date
* 2: Customer
* 3: I
* 4: Pay Method
* 5: Cash Paid
 #### open_short_tag_df
* 0: Ticket Number
* 1: License Plate or DL Number
* 2: Date Opened
* 3: Short Amount
 #### closed_short_tag_df
* 0: Operator
* 1: Ticket Number
* 2: Date Closed
* 3: Time Closed
* 4: Workstation
* 5: Cash Paid
