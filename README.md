# pycscale
## A Python module for PC Scale users who want cleaner, more accessible business data.

### An overview of the pypcscale module
The core purpose of pycscale is to provide an easy way for PC Scale users to access their transaction/ticket/customer data and convert
it to more flexible formats, allowing them to run custom reports, track new metrics, and integrate their data with in-house scripts and
applications. The pypcscale module does not rely on any direct connection to the SQL server holding your PC Scale company file. In fact,
pypcscale has been specifically designed not to touch the SQL database at all. (At least not directly).

How does pypcscale safely recreate an accurate snapshot of your company data without touching the SQL database? Well, it's very cutting-
edge: it asks you to run a few standard PC Scale reports, then cleans and combines the data from those reports into neatly-organized and
well-labeled pandas dataframes. These dataframes are stored in classes with methods that make it simple and intuitive to access, filter,
visualize, convert, and export the data.

To get the most out of pypcscale's functionality, the user should be familiar with Numpy arrays and pandas dataframes - especially with
respect to boolean indexing, which provides the easiest means of filtering data and running custom reports with specific constraints. 
Familiarity with Numpy and Pandas also makes it easier to process data and perform one-to-one mathematical operations on corresponding
row/column slices. To produce custom data visualizations (rather than those that come included as member functions), it also doesn't
hurt to be comfortable with Matplotlib.

Pypcscale is a pandas-based module. Pandas was chosen because of its flexibility; I wanted to give users the ability to manipulate
large ticket datasets easily using pandas dataframes, then take advantage of the myriad of possibilities from there. With a clean, well-
formatted pandas dataframe, the things you can do with your data are limited only by your imagination. My favorite features are the
ability to create and save your custom reports as reusable pandas queries/masks, lightning-fast csv or excel exports for coworkers who
are more comfortable working with spreadsheet data, and easy integration with Matplotlib for clear, appealing data visualization.

The main challenge I encountered working with PC Scale data was finding the optimal process for combining standard reports into a
comprehensive dataframe. This involved choosing the best/simplest set of standard reports that could be combined to store the "full
picture" for each ticket, then creating the process to convert this data into a simple one-to-one table. For example, certain types
of tickets, like split-load tickets, are stored across multiple rows in the PC Scale SQL database, which makes the data somewhat
difficult to work with. One of the more challenging parts of the data-cleaning process was consolidating this information into a more
workable format.

In future versions, I'd like to give users the native ability to save these processed dataframes locally and on the cloud. If there is
any demand, I'd also like to extend pypcscale's functionality to include customer account, invoicing, and facility data. Ideally,
this could allow users to automate large parts of their account management and invoicing processes in addition to ticket reporting.
Looking further to the future, I would also love to make pypcscale "smarter" with respect to how it interprets the input reports; if
pypcscale could recognize column data and fit it to the output dataframe automatically, the initial configuration process would be 
quite a bit faster for users with nonstandard PC Scale data indices.

---
### Table of Contents
##### [Installing and Configuring pypcscale](#Installing-and-Configuring-pypcscale)
##### [Loading Ticket Data](#Loading-Ticket-Data)
##### [Default DataFrame Indexing](#Default-DataFrame-Indexing)
###### [Main DataFrame (main_df)](#Main-DataFrame-(main_df))
###### [Main Cash Ticket DataFrame (opr_cash_df)](#Main-Cash-Ticket-DataFrame)
###### [Open Short Tag DataFrame (open_short_tag_df)](Open-Short-Tag-DataFrame)
###### [Closed Short Tag DataFrame (closed_short_tag_df)](Closed-Short-Tag-DataFrame)
---

#### Installing and Configuring pypcscale
The pypcscale module can be installed using pip with the command *pip install pypcscale*.

Once pypcscale is installed, it should then be configured to work with the user's PC Scale database using the pypcscale.configure()
class, which allows the user to set constants that will show the module how to fit its methods to the way their PC Scale data is
structured.

#### Loading Ticket Data
This section describes the process of exporting the right PC Scale reports with the right configuration, then loading them into the
pypcscale module to transform them into workable data.

#### Default DataFrame Indexing
This section outlines how ticket data is organized before and after pypcscale formatting. It also briefly illustrates some of the ways
pypcscale handles awkward data formatting present in the PC Scale report data.

##### Main DataFrame
For readability, I have removed many of the columns containing redundant/junk data in the original export file from PC Scale. However, in its original format, the OBDC Import excel file will be indexed something like this (Note the multi-row formatting of the split load on ticket 142772):
| GH1_INBOUND_TICKET | GH1_CustAdd | GH1_INBOUND_CUSTOMER | GH1_CarrAdd | GH1_INBOUND_DATE | GH1_INBOUND_TIME_IN | GH1_INBOUND_IN_OPERATOR | GH1_INBOUND_TIME_OUT | GH1_INBOUND_OUT_OPERATOR | GH1_ShowGross | GH1_Tare | GH1_Net | GH1_GTons | GH1_TTons | GH1_NTons | GH1_INBOUND_TRUCK | GH1_Type | GH1_INBOUND_LICENSE | GH1_INBOUND_TRAILER | GH1_INBOUND_CUYDS | GH2_Sum_(\_IPDETAIL_QUANTITY_,__IPDETAIL_WASTE_) | GH2_IPDETAIL_WASTE | GH2_WasteLine | GH2_Units | GH2_Rate | GH2_Sum_(\_IPDETAIL_PRETAX_,__IPDETAIL_WASTE_) | DE_IPDETAIL_ORIGIN | DE_ORIGIN_NAME | DE_COUNTY_NAME | DE_IPDETAIL_PCT | PF_DEPInfo | PF_Comments | PF_SumTaxes | PF_TotalAmount |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|142771|Joe's Junk Removal, 123 Broad Street, Miami, FL 07115|JOESJUNKRE|Big Boy Carriers LLC, 225 Main Street, Ft. Lauderdale, FL 07122|11/2/2020|7:00:31 AM|Joe Operator|7:09:11 AM|Jane Operator|12500|10000|2500|6.25|5.00|1.25|21-14453|DUMPER|AX2L2F|21-14454|30|1.25|13C|Construction and Demolition Waste|TONS|124.00|155.00|0221|Palm Bay|Beach County|100.0|32-55124|Driver complained about waiting for assistance on open face|0.00|155.00|
|142772|Steve's Recycling, 143 Broad Street, Miami, FL 07115|STEVESRECY|Big Boy Carriers LLC, 225 Main Street, Ft. Lauderdale, FL 07122|11/2/2020|7:01:15 AM|Joe Operator|7:10:11 AM|Jane Operator|19500|15000|4500|9.75|7.50|2.25|21-28453|ROLL-OFF|AX4Z2F|21-15784|40|2.25|23|Vegetative Waste|TONS|124.00|279.00|0221|Palm Bay|Beach County|50.0|32-55444|Split load; waste coming from different areas|0.00|139.50|
|142772|Steve's Recycling, 143 Broad Street, Miami, FL 07115|STEVESRECY|Big Boy Carriers LLC, 225 Main Street, Ft. Lauderdale, FL 07122|11/2/2020|7:01:15 AM|Joe Operator|7:10:11 AM|Jane Operator|19500|15000|4500|9.75|7.50|2.25|21-28453|ROLL-OFF|AX4Z2F|21-15784|40|2.25|23|Vegetative Waste|TONS|124.00|279.00|0221|Boca Raton|Beach County|50.0|32-55444|Split load; waste coming from different areas|0.00|139.50|
---
After being formatted by pypcscale, the indexing looks like this (Note how pypcscale consolidates multi-row entries to make the DataFrame one-to-one):
| Ticket Number | Customer Address | Customer | Carrier Address | Weigh-in Date | Weigh-in Time | Weigh-in Operator | Weigh-out Time | Weigh-out Operator | Gross Weight lbs | Tare Weight lbs | Net Weight lbs | Gross Weight Tons | Tare Weight Tons | Net Weight Tons | Vehicle Number | Vehicle Type | License Plate | Trailer Number | Trailer Volume Yards | Sum Weight Tons | Bill Code 1 | Bill Code Description 1 | Charge Units 1 | Charge Rate 1 | Unrounded Total Charge | Origin Code 1 | Origin Municipality 1 | Origin County 1 | Percentage 1 | Carrier DEP Number | Ticket Comments | Tax Sum | Ticket Revenue | Cash? | Rounding Adjustment | Cash Charge | Cash Paid | Short? | Short Amount | Pay Type | Short Paid? | Short Paid Date | Updated? | Last Update | Split Load? | Percentage 2 | Origin 2 | County 2 | Bill Code 2 | Percentage 3 | Origin 3 | County 3 | Bill Code 3 | 
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|142771|Joe's Junk Removal, 123 Broad Street, Miami, FL 07115|JOESJUNKRE|Big Boy Carriers LLC, 225 Main Street, Ft. Lauderdale, FL 07122|11/2/2020|7:00:31 AM|Joe Operator|7:09:11 AM|Jane Operator|12500|10000|2500|6.25|5.00|1.25|21-14453|DUMPER|AX2L2F|21-14454|30|1.25|13C|Construction and Demolition Waste|TONS|124.00|155.00|0221|Palm Bay|Beach County|100.0|32-55124|Driver complained about waiting for assistance on open face|0.00|155.00|True|0.00|155.00|155.00|False|0.00|Visa|NaN|NaN|True|11/22/2020|False|0.0|NaN|NaN|NaN|NaN|NaN|NaN|NaN|
|142772|Steve's Recycling, 143 Broad Street, Miami, FL 07115|STEVESRECY|Big Boy Carriers LLC, 225 Main Street, Ft. Lauderdale, FL 07122|11/2/2020|7:01:15 AM|Joe Operator|7:10:11 AM|Jane Operator|19500|15000|4500|9.75|7.50|2.25|21-28453|ROLL-OFF|AX4Z2F|21-15784|40|2.25|23|Vegetative Waste|TONS|124.00|279.00|0221|Palm Bay|Beach County|50.0|32-55444|Split load; waste coming from different areas|0.00|279.00|False|0.00|0|0|False|0.00|Account Credit|NaN|NaN|True|11/22/2020|True|50.0|Boca Raton|Beach County|23|NaN|NaN|NaN|NaN|
---
For easier reference, here's a bulleted list summary of the formatting before and after processing. (An arrow means that the column is reindexed to the name on the right side, while no arrow indicates a new column added by pypcscale. In parentheses is the datatype or object type of the element saved in the pandas DataFrame).
* 0: GH1_INBOUND_TICKET -> Ticket Number (int)
* 1: GH1_CustAdd -> Customer Address (string)
* 2: GH1_INBOUND_CUSTOMER -> Customer (string)
* 3: GH1_CarrAdd -> Carrier Address (string)
* 4: GH1_INBOUND_DATE -> Weigh-in Date (datetime.date object)
* 5: GH1_INBOUND_TIME_IN -> Weigh-in Time (datetime.time object)
* 6: GH1_INBOUND_IN_OPERATOR -> Weigh-in Operator (string)
* 7: GH1_INBOUND_TIME_OUT -> Weigh-out Time (datetime.time object)
* 8: GH1_INBOUND_OUT_OPERATOR -> Weigh-out Operator (string)
* 9: GH1_ShowGross -> Gross Weight lbs (int)
* 10: GH1_Tare -> Tare Weight lbs (int)
* 11: GH1_Net -> Net Weight lbs (int)
* 12: GH1_GTons -> Gross Weight Tons (float)
* 13: GH1_TTons -> Tare Weight Tons (float)
* 14: GH1_NTons -> Net Weight Tons (float)
* 15: GH1_INBOUND_TRUCK -> Vehicle Number (string)
* 16: GH1_Type -> Vehicle Type (string)
* 17: GH1_INBOUND_LICENSE -> License Plate (string)
* 18: GH1_INBOUND_TRAILER -> Trailer Number (string)
* 19: GH1_INBOUND_CUYDS -> Trailer Volume Yards (float)
* 20: GH2_Sum_(_IPDETAIL_QUANTITY_,__IPDETAIL_WASTE_) -> Sum Weight Tons (float)
* 21: GH2_IPDETAIL_WASTE -> Bill Code 1 (string)
* 22: GH2_WasteLine -> Bill Code Description 1 (string)
* 23: GH2_Units -> Charge Units 1 (string)
* 24: GH2_Rate -> Charge Rate 1 (float)
* 25: GH2_Sum_(_IPDETAIL_PRETAX_,__IPDETAIL_WASTE_) -> Unrounded Total Charge (float)
* 26: DE_IPDETAIL_ORIGIN -> Origin Code 1 (string)
* 27: DE_ORIGIN_NAME -> Origin Municipality 1 (string)
* 28: DE_COUNTY_NAME -> Origin County 1 (string)
* 29: DE_IPDETAIL_PCT -> Percentage 1 (float)
* 30: PF_DEPInfo -> Carrier DEP Number (string)
* 31: PF_Comments -> Ticket Comments (string)
* 32: PF_SumTaxes -> Tax Sum (float)
* 33: PF_TotalAmount -> Ticket Revenue (float)
* 34: Cash? (bool)
* 35: Rounding Adjustment (float)
* 36: Cash Charge (float)
* 37: Cash Paid (float)
* 38: Short? (bool)
* 39: Short Amount (float)
* 40: Pay Type (string)
* 41: Short Paid? (bool)
* 42: Short Paid Date (datetime.date object)
* 43: Updated? (bool)
* 44: Last Update (datetime.datetime object)
* 45: Split Load? (bool)
* 46: Percentage 2 (float)
* 47: Origin 2 (string)
* 48: County 2 (string)
* 49: Bill Code 2 (string)
* 50: Percentage 3 (float)
* 51: Origin 3 (string)
* 52: County 3 (string)
* 53: Bill Code 3 (string)
---


#### Main Cash Ticket DataFrame
* 0: Ticket Number
* 1: Date
* 2: Customer
* 3: Pay Type
* 4: Cash Paid

#### Open Short Tag DataFrame
* 0: Ticket Number
* 1: License Plate or DL Number
* 2: Date Opened
* 3: Short Amount
* 
#### Closed Short Tag DataFrame
* 0: Operator
* 1: Ticket Number
* 2: Date Closed
* 3: Time Closed
* 4: Workstation
* 5: Cash Paid

---
### How to Use pypcscale
Provide instructions and examples. Include screenshots.

---
### Credits

---
### License

---
### Badges

---
### How to Contribute

---
### Tests

