import urllib.request


print('Beginning file download with urllib2...')

url = 'http://172.18.0.225/logs/Log2/14020500.CSV'  
urllib.request.urlretrieve(url, '\Users\iZac\Google Drive\coffee') 
