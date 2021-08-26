import requests
import re
from bs4 import BeautifulSoup

urls = [
    'https://www.fatsecret.co.id/resep/51932644-udang-tumis-brokoli/Default.aspx',
    'https://www.fatsecret.co.id/resep/51922050-sup-tahu-wortel/Default.aspx',
    'https://www.fatsecret.co.id/resep/51393439-oatbanana-cookies/Default.aspx',
    'https://www.fatsecret.co.id/resep/51352570-sup-tomat/Default.aspx',
]

for url in urls:

    res = requests.get(url)

    pattern = re.compile('("nutrition": \[)(.+)(?=])', re.MULTILINE | re.DOTALL)
    namepattern = re.compile('("name": ")([a-zA-Z0-9_ ]+)(?=",)')

    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        # 1. out of many scripts, we only need the <script> that contains
        # nutrition information 
        script = soup.find('script', text=pattern)
        if script:
            # 2. extract the nutrition information from the script
            nutriraw = pattern.search(str(script)).group(2)
            
            # 2b. take out the 'name' portion of the string
            name = namepattern.search(str(script)).group(2)

            # \r = return (modern days PC: Enter) \n = new line
            nutriraw = ''.join(nutriraw.splitlines())
            # 3. convert the raw nutrition information to a dictionary
            nutridict = eval(nutriraw)
            # {'@type': 'NutritionInformation', 
            # 'calories': '189 cal', 
            # 'carbohydrateContent': '17.51 g', 
            # 'cholesterolContent': '0 mg', ...}
            print(nutridict)
            # 4. create our csv ('w' = write; 'r' = 'read')
            # name = f'{url.split("/")[-2]}.csv'
            with open(f'{name}.csv', 'w') as csvfile:
                
                for key in nutridict.keys():
                    csvfile.write(f'{key}, {nutridict[key]}\n')
