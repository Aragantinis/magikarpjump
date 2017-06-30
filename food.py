import requests
import pandas
from bs4 import BeautifulSoup

myLevels = [
    50, # Oran Berry
    50, # Sitrus Berry
    50, # Pecha Berry
    50, # Rindo Berry
    50, # Wacan Berry
    50, # Leppa Berry
    50, # Rawst Berry
    50, # Aspear Berry
    50, # Razz Berry
    50, # Bluk Berry
    50, # Lava Cookie
    60, # Shalour Sable
    94, #  Lumiose Galette
    25, # Castelia Cone
    0, # Magikarp Biscuit
]
actual_berry = 0

page = requests.get('https://www.serebii.net/magikarpjump/food.shtml')
if (page.status_code == 200):
    soup = BeautifulSoup(page.content, 'html.parser')
    detailedList = soup.find('li', {'title': 'Detailed'})
    tables = detailedList.find_all('table', {'class': 'tab'})

    analisys = pandas.DataFrame(
        columns=(
            'Berry',
            'Level',
            'Jump Power (JP)',
            'C25',
            'C50',
            'C75',
            'CtM (Cost to Max)',
            'IiJP (Increase In JP)',
            'CtM/IiJP'
        )
    )

    for table in tables:
        df = pandas.DataFrame(columns=('level', 'power', 'cost'))
        food_name = table.find_all('td', {'class': 'fooinfo'})[0].getText()
        food_levels = table.find('table').find_all('tr')
        first = True
        for food_level in food_levels:
            if first:
                first = False
                continue
            level = food_level.find_all('td')[0].getText()
            level = level.replace(',','')
            level = int(level)
            power = food_level.find_all('td')[1].getText()
            power = power.replace(',','')
            power = int(power)
            cost = food_level.find_all('td')[2].getText()
            cost = cost.replace(',','')
            cost = int(cost)
            df.loc[len(df.index)] = [level, power, cost]
        actual_level = df[df['level'] == myLevels[actual_berry]]
        to_upgrade = df[df['level'] > myLevels[actual_berry]]
        if myLevels[actual_berry] < 25:
            c25 = to_upgrade[to_upgrade['level'] < 26]
            c25 = c25['cost'].sum()
        else:
            c25 = 0
        if myLevels[actual_berry] < 50:
            c50 = to_upgrade[to_upgrade['level'] < 51]
            c50 = c50['cost'].sum()
        else:
            c50 = 0
        if myLevels[actual_berry] < 75:
            c75 = to_upgrade[to_upgrade['level'] < 76]
            c75 = c75['cost'].sum()
        else:
            c75 = 0
        analisys.loc[actual_berry] = [
            food_name,
            myLevels[actual_berry],
            actual_level['power'].sum(),
            c25,
            c50,
            c75,
            to_upgrade['cost'].sum(),
            to_upgrade['power'].sum(),
            to_upgrade['cost'].sum()/float(to_upgrade['power'].sum())
        ]
        actual_berry = actual_berry + 1
    print(analisys)
    print(analisys.info())
    print('Cost to 25: {}'.format(analisys['C25'].sum()))
    print('Cost to 50: {}'.format(analisys['C50'].sum()))
    print('Cost to 75: {}'.format(analisys['C75'].sum()))
    print('Cost to Max: {}'.format(analisys['CtM (Cost to Max)'].sum()))
