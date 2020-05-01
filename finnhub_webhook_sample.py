import requests

# Register new webhook for earnings
r = requests.post('https://finnhub.io/api/v1/webhook/add?token=bql9nt7rh5rfdbi8mhm0', json={'event': 'earnings', 'symbol': 'AAPL'})
res = r.json()
print(res)

webhook_id = res['id']
# List webhook
r = requests.get('https://finnhub.io/api/v1/webhook/list?token=bql9nt7rh5rfdbi8mhm0')
res = r.json()
print(res)

#Delete webhook
r = requests.post('https://finnhub.io/api/v1/webhook/delete?token=bql9nt7rh5rfdbi8mhm0', json={'id': webhook_id})
res = r.json()
print(res)

r = requests.get('https://finnhub.io/api/v1/stock/candle?symbol=$DJI&resolution=1&from=1572651390&to=1572910590&token=bql9nt7rh5rfdbi8mhm0')
print(r.json())