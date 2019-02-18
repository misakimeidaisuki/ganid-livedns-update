Gandi LiveDNS 動態更新IPv4/v6 IP腳本  

套件需求(Requirement)  
  configparser  
  ipaddress  
  requests  

執行程式(run the script)  
(或是使用cron)  
(You can also run it as a cron job)  
```
python3 live-dns-update.py
```



設定檔案範例(setting.conf example)  

各API與Gandi LiveDNS位置與金鑰,IPv4/IPv6 API需為純文字網頁  
Each API and Gandi LiveDNS URL/KEY, IPv4/IPv6 URL must output as text.  

```
[setting]  
API_url = https://dns.api.gandi.net/api/v5/    
API_Key = your_api_key                        
IPv4_address_api = https://api.ipify.org      
IPv6_address_api = http://v6.ipv6-test.com/api/myip.php P

```  

支援更新多個domain, 使用[domain_name]新增多的doamin,支援同時更新多筆 A 與 AAAA, 須以 json格式填寫。  
如果無法取得IPv4/v6時並不會更新A/AAAA紀錄  
It can update multi domain.  
Using [domain_name] to add another domain which you want to update it.  
It also can update multi A/AAAA record at the same time, but must use json format.  
When cannot get the IPv4/v6 address, it will not update A/AAAA records.  

格式(format)  
```
[domain_name]
A = {"record_a": TTL }  
AAAA = = {"record_a": TTL }
```

TTL需大於300(s)以上
The TTL must more than 300s.

```
[example.com]
A = {
 "@": 300,
 "www": 300}

AAAA = {
 "@": 300,
 "www": 300}

[example2.com]
A = {
 "@": 300,
 "www": 300}

AAAA = {
 "@": 300,
 "www": 300}

 ...

```
