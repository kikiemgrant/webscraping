import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

URL = 'https://www.premierleague.com'
page = requests.get(URL + '/clubs')
soup = BeautifulSoup(page.content, 'html.parser')

clubTags = soup.find_all('a', {'class': 'indexItem'})
clubs = []
for tag in clubTags:
    clubURL = URL + tag['href']
    clubURL = clubURL.replace("overview", "squad")
    clubs.append(clubURL)


# loop through each club, appending the link to each players web page to the list 'playerOverviews'
playerOverviews = []
for club in clubs:
    while True:
        # import and parse club web pages, find all 'a' tags
        try:
            clubPage = requests.get(club)
            clubSoup = BeautifulSoup(clubPage.content, 'html.parser')
            playerTags = clubSoup.find_all('a', {'class': 'playerOverviewCard'})

            # grabs links to each players web page and append to list 'playerOverviews'
            for tag in playerTags:
                playerURL = URL + tag['href']
                playerOverviews.append(playerURL)
            break
        # exception written for the case that data is requested too frequently from pages
        except:
            time.sleep(5)
            continue

# empty lists for all data we want to grab
names = []
clubs = []
ages = []
heights = []
weights = []
nations = []
positions = []

# list of valid positions
validPositions = ['Goalkeeper', 'Midfielder', 'Defender', 'Forward']

# loop through every player link in list 'playerOverviews'
# import and parse players web page
# find data and add to list
# if there is an exception (i.e. data doesn't exist) append 'None'
for playerURL in playerOverviews:
    playerPage = requests.get(playerURL)
    playerSoup = BeautifulSoup(playerPage.content, 'html.parser')

    # scrape names
    try:
        playerName = playerSoup.find_all('div', {'class': 'name'})
        playerName = playerName[0].text.strip()
        names.append(playerName)
    except:
        names.append(None)

    # scrape clubs
    try:
        playerClub = playerSoup.find_all('td', {'class': 'team'})
        playerClub = playerClub[0].find_all('span', {'class': 'short'})
        playerClub = playerClub[0].text.strip()
        clubs.append(playerClub)
    except:
        clubs.append(None)

    # scrape positions
    try:
        temp = playerSoup.find_all('div', {'class': 'info'})
        tempPosition = temp[1].text.strip()
        if tempPosition in validPositions:
            playerPosition = tempPosition
        else:
            tempPosition = temp[0].text.strip()
            playerPosition = tempPosition
        positions.append(playerPosition)
    except:
        positions.append(None)

    # scrape ages
    try:
        playerAge = playerSoup.find_all('ul', {'class': 'pdcol2'})
        playerAge = playerAge[0].find_all('span', {'class': 'info--light'})
        playerAge = playerAge[0].text.strip().replace('(', '').replace(')', '')
        ages.append(playerAge)
    except:
        ages.append(None)

    # scrape heights
    try:
        playerPhysical = playerSoup.find_all('ul', {'class': 'pdcol3'})
        playerPhysical = playerPhysical[0].find_all('div', {'class': 'info'})
        playerHeight = playerPhysical[0].text.strip()
        heights.append(playerHeight)
    except:
        heights.append(None)

    # scrape weights
    try:
        playerPhysical = playerSoup.find_all('ul', {'class': 'pdcol3'})
        playerPhysical = playerPhysical[0].find_all('div', {'class': 'info'})
        playerWeight = playerPhysical[1].text.strip()
        weights.append(playerWeight)
    except:
        weights.append(None)

    # scrape nationalities
    try:
        playerNation = playerSoup.find_all('ul', {'class': 'pdcol1'})
        playerNation = playerNation[0].find_all('div', {'class': 'info'})
        playerNation = playerNation[0].text.strip()
        nations.append(playerNation)
    except:
        nations.append(None)

# create dictionary containing all lists as well as headers
d = {
    'Name': names,
    'Position': positions,
    'Club': clubs,
    'Nationality': nations,
    'Age': ages,
    'Height': heights,
    'Weight': weights
    }
# dictionary -> dataframe
playerOverview = pd.DataFrame(d)

playerOverview.dropna(axis = 0, inplace = True)
playerOverview.reset_index(drop=True, inplace=True)

loan = []
for i in range(len(playerOverview)):
    club = playerOverview['Club'][i]
    if '(Loan)' in club:
        loan.append(True)
        club = club.replace('(Loan)', '')
        playerOverview['Club'][i] = club
    else:
        loan.append(False)
playerOverview['On Loan'] = loan

# remove suffixes from columns
for i in range(len(playerOverview)):
    height = playerOverview['Height'][i]
    newHeight = ''
    for letter in height:
        if not(letter.isalpha()):
            newHeight += letter
    playerOverview['Height'][i] = newHeight
    weight = playerOverview['Weight'][i]
    newWeight = ''
    for letter in weight:
        if not(letter.isalpha()):
            newWeight += letter
    playerOverview['Weight'][i] = newWeight

playerOverview.rename(columns={'Height': 'Height (cm)', 'Weight': 'Weight (kg)'}, inplace=True)

playerOverview['Age'] = playerOverview['Age'].astype(int)
playerOverview['Height (cm)'] = playerOverview['Height (cm)'].astype(int)
playerOverview['Weight (kg)'] = playerOverview['Weight (kg)'].astype(int)

playerOverview.to_csv(r'C:\Users\kyrae\Documents\GitHub\webscraping\playerOverviews.csv')
print("Done")