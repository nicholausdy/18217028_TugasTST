
# coding: utf-8

# In[20]:


import requests
r = requests.get("https://192.168.56.110:10400",verify='/home/jupyter/certificate2.pem',headers={'Authorization': 'Basic YW5vdGhlcjptZQ=='})
print(r.status_code)
print(r.headers)
print(r.content)

