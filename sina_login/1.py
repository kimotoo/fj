
import re
import time

url = "https://weibo.com/6632894984/GyxpGgGcF?from=page_1005056632894984_profile&wvr=6&mod=weibotime&type=comment#_rnd1536467344330"

pde = re.findall(r'page_(.*?)_' ,url)[0]

print(time.time()*1000)
print(1536469345873)