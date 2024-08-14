import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import warnings

warnings.simplefilter('ignore', InsecureRequestWarning)

response = requests.get('https://www.imsnsit.org/imsnsit/notifications.php', verify=False)
print(response.content)
