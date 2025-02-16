import requests
import datetime
import matplotlib.pyplot as plt
import pandas as pd

address = '0x9FC3da866e7DF3a1c57adE1a97c9f00a70f010c8'  
api_key = 'myApi' 

url = "https://api.etherscan.io/api"
params = {
    "module": "account",
    "action": "txlist",
    "address": address,
    "startblock": 0,
    "endblock": 99999999,
    "sort": "asc",
    "apikey": api_key
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    
    if data['status'] == '1':  
        transactions = data['result']
        
        timestamps = []
        values = []
        gas_paid = []
        
        for tx in transactions:
            timestamp = int(tx['timeStamp'])
            time = datetime.datetime.utcfromtimestamp(timestamp)
            timestamps.append(time)
            
            value = int(tx['value']) / 10**18  
            values.append(value)
            
            gas_used = int(tx['gasUsed'])
            gas_price = int(tx['gasPrice']) / 10**18  
            total_gas_paid = gas_used * gas_price  
            gas_paid.append(total_gas_paid)
        
        df = pd.DataFrame({
            'Timestamp': timestamps,
            'Value (ETH)': values,
            'Gas Paid (ETH)': gas_paid
        })
        
        plt.figure(figsize=(10, 5))
        plt.plot(df['Timestamp'], df['Value (ETH)'], marker='o', linestyle='-', color='b', label='Transaction Value (ETH)')
        plt.title('Account Time vs Ether(ETH) Value')
        plt.xlabel('Timestamp')
        plt.ylabel('Transaction Value (ETH)')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.show()
        
        plt.figure(figsize=(10, 5))
        plt.plot(df['Timestamp'], df['Gas Paid (ETH)'], marker='s', linestyle='-', color='r', label='Gas Paid (ETH)')
        plt.title('Account Time vs Gas Paid (ETH)')
        plt.xlabel('Timestamp')
        plt.ylabel('Gas Paid (ETH)')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.show()
    else:
        print("Error fetching transactions:", data.get('message', 'Unknown error'))
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
