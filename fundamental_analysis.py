import streamlit as st
import pandas as pd
import requests
import numpy as np

from bs4 import BeautifulSoup
import pandas as pd
def read_stock_list(file_path):
    with open(file_path, 'r') as file:
        stock_list = file.read().splitlines()
    return stock_list

# Path to the stock_list.txt file
file_path = 'stock_list.txt'

# Read the stock list
stock_list = read_stock_list(file_path)

st.title("STOMKS by wuzuki_tan")
choice=st.selectbox("Enter your choice",stock_list)


url = f'https://www.screener.in/company/{choice}/consolidated/#profit-loss'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('section', {'id': 'balance-sheet'}).find('table')

# Extract table headers
headers = [header.text.strip() for header in table.find_all('th')]

# Extract table rows
rows = []
for row in table.find_all('tr')[1:]:  # Skip the header row
    data = [cell.text.strip() for cell in row.find_all('td')]
    rows.append(data)

# Create a pandas DataFrame
df = pd.DataFrame(rows, columns=headers)
df.replace({"":np.nan},inplace=True)
df.dropna(axis=1,inplace=True)
df_transposed = df.transpose()
df_transposed.reset_index(inplace=True)
df_transposed.columns = df_transposed.iloc[0]
df_transposed = df_transposed[1:].reset_index(drop=True)
df_transposed.insert(loc=0,column='year',value=df_transposed[''])

df_transposed.drop([''],axis=1,inplace=True)
df=df_transposed
final_df=df.tail(2)

def year_change(year):
  return(year[4:])
final_df['year'] = final_df['year'].apply(year_change)
final_df = final_df.replace(',', '', regex=True).astype(float)

final_df = final_df.replace(',', '', regex=True).astype(float)

st.header("BALANCE SHEET ANALYSIS")
st.subheader("Reserves Analysis")
n=list(final_df['Reserves'])[1]
o=list(final_df['Reserves'])[0]
if n>o :
  st.write(f"The company reserves increased from ",o," to ",n," which indicates that the company is retaining more earnings for future use,which can strengthen its financial position and provide a cushion for future expenses or investments.")
else:
  st.write(f"Reserves decreased from ",o," to ",n," which may suggest that the company is using its reserves to cover losses, pay dividends, or fund investments, which could weaken its financial stability if not managed properly")  


st.subheader('Borrowings Analysis')
n=final_df.iloc[1,3]
o=final_df.iloc[0,3]
if n>o:
  st.write(f"There is an increase in the borrowings from {o}Cr. to {n}Cr. which suggests that the company is taking on more debt to finance its operations or investments. This could indicate expansion but also increases financial risk due to higher interest obligations.")
else:
  st.write("Decrease in borrowing indicates that the company is paying off its debts, reducing financial risk and interest expenses, which can improve profitability and financial health.")  

st.subheader('Total Liabilities Analysis')
n=final_df.iloc[1,5]
o=final_df.iloc[0,5]
if n>o:
  st.write(f"There is an increase in the total liabilities from {o}Cr. to {n}Cr. which reflects an overall rise in the company's financial obligations, which could indicate growth and expansion but also increases financial risk.")
else:
  st.write(f"Decrease in total liabilites from {o}Cr. to {n}Cr. indicates a reduction in the company's financial obligations, improving its balance sheet and reducing financial risk.")

st.subheader('Fixed Asset Analysis')
n=final_df.iloc[1,6]
o=final_df.iloc[0,6]
if n>o:
  st.write(f"There is an increase in fixed assets from {o}Cr. to {n}Cr. signalling investments in long-term assets like property or equipment, supporting future growth and operational efficiency.")
else:
  st.write(f"Seems a decrease in fixed assets which may indicate asset sales or impaired assets. While divestment can streamline operations, persistent decreases might suggest underinvestment or industry challenges.")

st.subheader("CWIP Analysis")
n=final_df.iloc[1,7]
o=final_df.iloc[0,7]
if n>o:
  st.write(f"The cwip has increased from {o}Cr. to {n}Cr. suggests that the company is investing in new assets or expanding its operations. Investors may view this as a positive sign of growth and future revenue potential.")
else:
  st.write(f"CWIP decreased from {o}Cr. to {n}Cr. which means projects are nearing completion.Completed assets contribute to revenue and profitability. Investors may see this positively, especially if the projects were capital-intensive.")  

st.subheader("Total Assets Analysis")
n=final_df.iloc[1,10]
o=final_df.iloc[0,10]
change=abs(((abs(n)-abs(o))/abs(o))*100)
if n>o:
  st.write(f" There is an increase in total assets from {o} Cr. to {n} Cr. which is {change}% increase .Growing assets often indicate business expansion or successful operations. Investors may view this as a sign of growth and potential.However, it’s essential to consider how these assets are financed. If they result from increased revenue or efficient operations, it’s favorable. If they’re funded by debt, it could raise concerns")
else:
   st.write(f"There is a decrease in it from {o} Cr to {n} Cr which is {change}% decrease. A decrease in assets might signal divestments, asset write-offs, or operational challenges. Investors should investigate the reasons behind the decline.")

table = soup.find('section', {'id': 'cash-flow'}).find('table')

# Extract table headers
headers = [header.text.strip() for header in table.find_all('th')]

# Extract table rows
rows = []
for row in table.find_all('tr')[1:]:  # Skip the header row
    data = [cell.text.strip() for cell in row.find_all('td')]
    rows.append(data)
import numpy as np
# Create a pandas DataFrame
df = pd.DataFrame(rows, columns=headers)
df.replace({"":np.nan},inplace=True)
df.dropna(axis=1,inplace=True)
df_transposed = df.transpose()

# Reset the index
df_transposed.reset_index(inplace=True)
df_transposed.columns = df_transposed.iloc[0]
df_transposed = df_transposed[1:].reset_index(drop=True)
df_transposed.insert(loc=0,column='year',value=df_transposed[''])

df_transposed.drop([''],axis=1,inplace=True)
df=df_transposed
def year_change(year):
  return(year[4:])
df['year'] = df['year'].apply(year_change)

df = df.replace(',', '', regex=True).astype(float)

final_df=df.tail(2)
df.drop("year",axis=1,inplace=True)
st.header("Cash Flow Analysis")
st.line_chart(df)
st.subheader("Operational Activities")
n=final_df.iloc[1,1]
o=final_df.iloc[0,1]
change=int(abs(((abs(n)-abs(o))/abs(o))*100))
if n>o:
   st.write(f"There is an increase in operational cash from {o} to {n} which is an increase of {change}% .An increase indicates that the company is more effectively converting its sales and services into actual cash inflows. This could result from higher revenues, better management of receivables and payables, or cost reductions. A steady increase suggests that the company has a healthy cash flow, which can be used for reinvestment, paying down debt, paying dividends, or other strategic initiatives.")
else:
   st.write(f"There is a decrease in operational cash of {change}%. A decrease might indicate issues in generating cash from the company's core operations, such as declining sales or increased operating expenses. ")
st.subheader("Investment Activities")
n=final_df.iloc[1,2]
o=final_df.iloc[0,2]
change=int(abs(((abs(n)-abs(o))/abs(o))*100))
if n>o:
   st.write(f"Increase of investment activites by {change}%.  An increase typically indicates that the company is selling off assets, such as property, plant, equipment, or investments. This can be a sign of asset reallocation or divestment. Mature Investments: Cash inflow from the maturity or sale of investments can lead to an increase in this area. Divestiture Strategy: If the company is consistently increasing cash from investing activities, it might be focusing on divesting non-core or underperforming assets to streamline operations or raise cash. Liquidation for Liquidity Needs: In some cases, an increase might indicate that the company is selling assets to raise cash to cover operational shortfalls or to improve liquidity.")
else:
   st.write(f"There is a decrease of {change}% from {o} to {n}.A decrease usually indicates that the company is spending more on purchasing fixed assets, such as property, plant, equipment, or technology, which can signal investment in growth and expansion. Acquisitions: Spending cash on acquisitions of other companies or investments in joint ventures or partnerships will result in a decrease.")   
st.subheader("Finance Activities")
n=final_df.iloc[1,3]
o=final_df.iloc[0,3]
change=int(abs(((abs(n)-abs(o))/abs(o))*100))
if n>o:
   st.write(f"There is an increase of cash from Finance Activities from {o} to {n} i.e a {change}% increase.An increase often indicates that the company is raising funds through borrowing. This could be through issuing bonds, taking loans, or other forms of debt.Raising cash through financing can indicate that the company is gearing up for expansion, acquisitions, or other significant investments. Companies may increase cash from financing activities to improve liquidity, ensuring they have enough cash on hand to meet operational needs or handle unexpected expenses.")
else:
   st.write(f"There is a decrease of {change}%. A decrease often indicates that the company is using cash to pay down existing debt, which reduces its liabilities.A decrease can signify that the company has less need for external financing, possibly due to strong cash flows from operating activities.Distributing dividends to shareholders results in cash outflows and reflects the company’s commitment to returning value to its investors.")

table = soup.find('section', {'id': 'shareholding'}).find('table')

# Extract table headers
headers = [header.text.strip() for header in table.find_all('th')]

# Extract table rows
rows = []
for row in table.find_all('tr')[1:]:  # Skip the header row
    data = [cell.text.strip() for cell in row.find_all('td')]
    rows.append(data)

# Create a pandas DataFrame
df = pd.DataFrame(rows, columns=headers)
df_transposed = df.transpose()

# Reset the index
df_transposed.reset_index(inplace=True)
df_transposed.columns = df_transposed.iloc[0]
df_transposed = df_transposed[1:].reset_index(drop=True)
df_transposed.insert(loc=0,column='year',value=df_transposed[''])

df_transposed.drop([''],axis=1,inplace=True)
df=df_transposed

def year_change(year):
  return(year[4:])
df['year'] = df['year'].apply(year_change)
df.drop(['No. of Shareholders','year'],inplace=True,axis=1)
def remover(value):
  return value[:-1]
for i in range(0,len(df.columns)):
  df[df.columns[i]] = df[df.columns[i]].apply(remover)
df = df.replace(',', '', regex=True).astype(float)

final_df=df.tail(2)

st.header("Shareholding Pattern")
st.line_chart(df)
st.write(final_df)


# Define the search term
# Replace with your choice of news topic

import requests
from bs4 import BeautifulSoup

# URL of the news website
url = f'https://www.google.com/search?q={choice}+news&tbm=nws'

# Send a GET request to the URL
response = requests.get(url)

# Parse HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all headlines (usually within <h3> tags for news)
headlines = soup.find_all('h3')

# Print the headlines as hyperlinks
st.header(f"Recent news headlines for {choice}:")
c=0
for headline in headlines:
    a_tag = headline.find_parent('a')
    if a_tag and a_tag['href']:
        link = a_tag['href']
        # Clean up the link to remove Google redirect
        clean_link = link.split('&')[0].replace('/url?q=', '')
        st.markdown(f"**[{headline.get_text()}]({clean_link})**")
        c=c+1
    if c==5:
       break            
