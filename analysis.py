#importation of the libraries
from pypdf import PdfReader, PdfWriter
import pandas as pd
import numpy as np 
import pdfplumber
reader = PdfReader("MPESA_Statement_2026-06-13_to_2024-06-13_2541xxxxxx739-1.pdf")
# Enter your PDF password
reader.decrypt("932359")

writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

with open("unlocked_statement.pdf", "wb") as f:
    writer.write(f)

print("PDF unlocked!")

all_rows = []

with pdfplumber.open("unlocked_statement.pdf") as pdf:
    for page in pdf.pages:

        table = page.extract_table()

        if table:
            all_rows.extend(table)
df = pd.DataFrame(all_rows[1:], columns=all_rows[0])
print(df.info())
print(df.head())
print(df.shape)
print(df.isnull().sum())


df['Completion Time']= pd.to_datetime(df["Completion Time"],errors='coerce')#converting date 
df['Paid In'] = pd.to_numeric(df['Paid In'], errors='coerce')
df['Withdrawn'] = pd.to_numeric(df['Withdrawn'], errors='coerce')
df['Balance']=pd.to_numeric(df['Balance'],errors='coerce')
df['Net Amount'] = df['Paid In'].fillna(0) + df['Withdrawn'].fillna(0) 
df['Completion Time'] = pd.to_datetime(df['Completion Time'])

df['year'] = (
    df['Completion Time']
    .dt.year
)

df['month'] = (
    df['Completion Time']
    .dt.strftime('%Y-%m')
)

monthly = df.groupby(
    df['Completion Time'].dt.to_period('M')
).agg({
    'Paid In':'sum',
    'Withdrawn':'sum',
    'Net Amount':'sum'
})

print(monthly)
def categorize(details):
    details = str(details)

    if 'Funds sent' in details:
        return 'Income'

    elif 'OD Loan Repayment' in details:
        return 'Fuliza Repayment'

    elif 'KCB M-PESA Deposit' in details:
        return 'KCB Deposit'

   
    elif 'Merchant Payment' in details:
        return 'Buy Goods'

    elif 'Pay Bill' in details:
        return 'Paybill'
    elif 'Customer Payment' in details:
        return 'pochi la biashara'
    
    elif 'Customer Transfer' in details or 'Send Money' in details:
        return 'Send Money'
    elif 'Customer Transfer' in details or 'Send Money' in details:
            return 'Send Money'
    elif 'Airtime Purchase' in details:
            return 'Airtime'
    elif 'Customer Bundle Purchase' in details:
            return 'Bundles'
    elif 'Withdrawal Charge' in details or 'Transaction Charge' in details:
            return 'Charges'
    elif 'M-Shwari' in details:
            return 'Mshwari'
    else:
       return "others"

    
df['Spending'] = df['Details'].apply(categorize)
transaction_totals = (
    df.groupby('Spending')['Net Amount']
      .agg(['sum'])
      .sort_values('sum',ascending=False)
      .head(10)
)

print(transaction_totals)


def recipient(details):
    details =str(details)
    if details.strip() == 'details':
        return None
    if "Funds received" in details:
        return "Income"
    elif 'OverDraft of Credit Party' in details:
        return 'Fuliza credit'
    elif 'KCB M-PESA Withdraw' in details:
        return 'KCB Withdrawal'
    elif "M-shwari Withdraw" in details:
        return 'Mshwari withdrawal'
    elif 'Deposit of Funds at Agent' in details:
        return "Agent deposit"
    
    else :
        return 'others'
df['received'] = df['Details'].apply(recipient)
recieved=(
    df.groupby('received')['Net Amount']
      .agg(['sum'])
      .sort_values('sum',ascending=False)
)
print(recieved)
print('Cash In is:',df['Paid In'].sum())
print('Cash Out is:',df['Withdrawn'].sum())
df.to_csv('M_PESA_statement.csv',index=False)

