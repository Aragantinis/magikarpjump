import requests
import pandas
from bs4 import BeautifulSoup

myLevels = [
    35,
    30,
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    25,
    25,
]
actual_training = 0

page = requests.get('https://www.serebii.net/magikarpjump/training.shtml')
if (page.status_code == 200):
    soup = BeautifulSoup(page.content, 'html.parser')
    detailedList = soup.find('li', {'title': 'Detailed'})
    tables = detailedList.find_all('table', {'class': 'tab'})

    analisys = pandas.DataFrame(
        columns=(
            'Training',
            'Level',
            'Production',
            'C25',
            'C50',
            'C75',
            'CtM (Cost to Max)',
            'IiP (Increase In Production)',
            'CtM/IiP'
        )
    )

    for table in tables:
        df = pandas.DataFrame(columns=('level', 'power', 'cost'))
        train_name = table.find_all('td', {'class': 'fooinfo'})[0].getText()
        train_levels = table.find('table').find_all('tr')
        first = True
        for train_level in train_levels:
            if first:
                first = False
                continue
            level = train_level.find_all('td')[0].getText()
            level = level.replace(',','')
            level = int(level)
            power = train_level.find_all('td')[1].getText()
            power = power.replace(',','')
            power = int(power)
            cost = train_level.find_all('td')[2].getText()
            cost = cost.replace(',','')
            cost = int(cost)
            df.loc[len(df.index)] = [level, power, cost]
        actual_level = df[df['level'] == myLevels[actual_training]]
        to_upgrade = df[df['level'] > myLevels[actual_training]]
        if myLevels[actual_training] < 25:
            c25 = to_upgrade[to_upgrade['level'] < 26]
            c25 = c25['cost'].sum()
        else:
            c25 = 0
        if myLevels[actual_training] < 50:
            c50 = to_upgrade[to_upgrade['level'] < 51]
            c50 = c50['cost'].sum()
        else:
            c50 = 0
        if myLevels[actual_training] < 75:
            c75 = to_upgrade[to_upgrade['level'] < 76]
            c75 = c75['cost'].sum()
        else:
            c75 = 0
        analisys.loc[actual_training] = [
            train_name,
            myLevels[actual_training],
            actual_level['power'].sum(),
            c25,
            c50,
            c75,
            to_upgrade['cost'].sum(),
            to_upgrade['power'].sum(),
            to_upgrade['cost'].sum()/float(to_upgrade['power'].sum())
        ]
        actual_training = actual_training + 1
    print(analisys)
    print(analisys.info())
    print('Cost to 25: {}'.format(analisys['C25'].sum()))
    print('Cost to 50: {}'.format(analisys['C50'].sum()))
    print('Cost to 75: {}'.format(analisys['C75'].sum()))
    print('Cost to Max: {}'.format(analisys['CtM (Cost to Max)'].sum()))
