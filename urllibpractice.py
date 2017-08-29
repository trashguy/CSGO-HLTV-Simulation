# Made by Austin Moore
# Not GPL yet

import re # Regular expression parsing
import urllib.request # Opening page URLs
import math # Using the floor() function
import numpy # Using nextafter() function

class player:
    def __init__(self):
        self.name = 'Kirk'
        self.kills = 0
        self.deaths = 0
        self.rounds = 0
        self.kdr = 0.0 # Kill-Death Ratio
        self.dkr = 0.0 # Death-Kill Ratio
        self.kpr = 0.0 # Kills Per Round
        self.dpr = 0.0 # Deaths Per Round
        self.hltv_rating = 0.0
        self.inv_hltv_rating = 0.0
        self.url = ' '
        self.stats_url = ' '
        self.negative = 0.0 # Either dkr, dpr, or inv_hltv_rating
        self.positive = 0.0 # Either kdr, kpr, or hltv_rating
        self.lower_negative_range = 0.0
        self.upper_negative_range = 0.0
        self.lower_positive_range = 0.0
        self.upper_positive_range = 0.0
        self.alive = True
        
class team:
    def __init__(self):
        self.won_rounds = 0
        self.lost_rounds = 0
        self.wins = 0
        self.losses = 0
        self.name = 'A-Team'
        self.player_count = 5
        self.players = [player() for i in range(self.player_count)]
        self.url = ' '
        self.team_negative = 0.0 # The addition of all negative on ONE team

class game:
    def __init__(self):
        self.bestof = 1
        self.rounds = 30
        self.team_count = 2
        self.teams = [team() for i in range(self.team_count)]
        self.score = ['0-0']
        self.score_index = 0

# Open the URL and save it to page
url = input('Enter the HLTV URL: ')
user_agent_spoof = {'User-Agent':'Mozilla/5.0'}
req = urllib.request.Request(url, headers=user_agent_spoof)
page = urllib.request.urlopen(req).read()
page = page.decode('utf-8')

# Create the game
the_game = game()

# Find and save team names
for i in range(the_game.team_count):
    the_game.teams[i].name = re.findall(r'<div class="team' + str(i + 1) + '-gradient">.*<img alt="(.*)" src', page)
    the_game.teams[i].name = the_game.teams[i].name[0]
    print('Team ' + str(i + 1) + ' name: ' + the_game.teams[i].name)

# Find the url to all teams
for i in range(the_game.team_count):
    the_game.teams[i].url = re.findall(r'<div class="team' + str(i + 1) + '-gradient"><a href="(/\w*/\d*/.*)"><img', page)
    the_game.teams[i].url = the_game.teams[i].url[0]
    the_game.teams[i].url = 'https://www.hltv.org' + the_game.teams[i].url
    print('Team ' + str(i + 1) + ' URL: ' + the_game.teams[i].url)

print()

# Team loop
# Get player stats
for i in range(the_game.team_count): # Open the URL to the teams one at a time
    req = urllib.request.Request(the_game.teams[i].url, headers=user_agent_spoof)
    page = urllib.request.urlopen(req).read()
    page = page.decode('utf-8')

    # Get player names and URLs
    player_names = re.findall(r'class="text-ellipsis">(.*)</a>', page)
    player_urls = re.findall(r'<a href="(/\w*/\d*/.*)" class', page)
    # Append hltv.org to all URLs
    for i2 in range(len(player_urls)):
        player_urls[i2] = 'https://www.hltv.org' + player_urls[i2]

    # Player loop
    # Assign player names, URLs, and stats to player objects
    for i2 in range(the_game.teams[i].player_count):
        # Assign names and main page URLs
        the_game.teams[i].players[i2].name = player_names[i2]
        the_game.teams[i].players[i2].url = player_urls[i2]
        print('Player ' + str(i2 + 1) + ' name: ' + the_game.teams[i].players[i2].name)
        print('Player ' + str(i2 + 1) + ' URL: ' + the_game.teams[i].players[i2].url)
        
        # Open main player URLs and assign the URL to their detailed stats
        req = urllib.request.Request(the_game.teams[i].players[i2].url, headers=user_agent_spoof)
        page = urllib.request.urlopen(req).read()
        page = page.decode('utf-8')
        
        # Assign detailed stats URLs
        the_game.teams[i].players[i2].stats_url = re.findall(r'<a href="(/\w*/\w*/\d*/.*)" class', page)
        the_game.teams[i].players[i2].stats_url = the_game.teams[i].players[i2].stats_url[0]
        the_game.teams[i].players[i2].stats_url = 'https://www.hltv.org' + the_game.teams[i].players[i2].stats_url
        print('Player ' + str(i2 + 1) + ' detailed URL: ' + the_game.teams[i].players[i2].stats_url)

        # Open the detailed stats URLs
        req = urllib.request.Request(the_game.teams[i].players[i2].stats_url, headers=user_agent_spoof)
        page = urllib.request.urlopen(req).read()
        page = page.decode('utf-8')

        # Grab player stats
        # Grab kills
        the_game.teams[i].players[i2].kills = re.findall(r'<div class="stats-row"><span>total kills</span><span>(\d*)', page, re.I)
        the_game.teams[i].players[i2].kills = int(the_game.teams[i].players[i2].kills[0])
        print('Player ' + str(i2 + 1) + ' kills: ' + str(the_game.teams[i].players[i2].kills))

        # Grab deaths
        the_game.teams[i].players[i2].deaths = re.findall(r'<div class="stats-row"><span>Total deaths</span><span>(\d*)', page, re.I)
        the_game.teams[i].players[i2].deaths = int(the_game.teams[i].players[i2].deaths[0])
        print('Player ' + str(i2 + 1) + ' deaths: ' + str(the_game.teams[i].players[i2].deaths))

        # Grab rounds
        the_game.teams[i].players[i2].rounds = re.findall(r'<div class="stats-row"><span>Rounds played</span><span>(\d*)', page, re.I)
        the_game.teams[i].players[i2].rounds = int(the_game.teams[i].players[i2].rounds[0])
        print('Player ' + str(i2 + 1) + ' rounds: ' + str(the_game.teams[i].players[i2].rounds))

        # Grab HLTV Rating
        the_game.teams[i].players[i2].hltv_rating = re.findall(r'"strong">(.*)</span></div>', page, re.I)
        the_game.teams[i].players[i2].hltv_rating = float(the_game.teams[i].players[i2].hltv_rating[0])
        print('Player ' + str(i2 + 1) + ' HLTV Rating: ' + str(the_game.teams[i].players[i2].hltv_rating))

        # Calculate kdr
        the_game.teams[i].players[i2].kdr = the_game.teams[i].players[i2].kills / the_game.teams[i].players[i2].deaths
        print('Player ' + str(i2 + 1) + ' KDR: ' + str(the_game.teams[i].players[i2].kdr))

        # Calculate dkr
        the_game.teams[i].players[i2].dkr = the_game.teams[i].players[i2].deaths / the_game.teams[i].players[i2].kills
        print('Player ' + str(i2 + 1) + ' DKR: ' + str(the_game.teams[i].players[i2].dkr))

        # Calculate kpr
        the_game.teams[i].players[i2].kpr = the_game.teams[i].players[i2].kills / the_game.teams[i].players[i2].rounds
        print('Player ' + str(i2 + 1) + ' KPR: ' + str(the_game.teams[i].players[i2].kpr))

        # Calculate dpr
        the_game.teams[i].players[i2].dpr = the_game.teams[i].players[i2].deaths / the_game.teams[i].players[i2].rounds
        print('Player ' + str(i2 + 1) + ' DPR: ' + str(the_game.teams[i].players[i2].dpr))

        # Calculate inv_hltv_rating
        the_game.teams[i].players[i2].inv_hltv_rating = pow(the_game.teams[i].players[i2].hltv_rating, (-1))
        print('Player ' + str(i2 + 1) + ' Inverse HLTV Rating: ' + str(the_game.teams[i].players[i2].inv_hltv_rating))

        
        print()

# Calculate the likelihood that a player is to get a kill or die
def calculate_player_range():
    negative_upper = 0.0 # The current number to set the next player's lower_negative_range
    positive_upper = 0.0 # The current number to set the next player's lower_positive_range
    total_positive = 0.0 # The addition of all positive on each team

    # Find total_positive and total_negative (for the teams)
    for i in range(the_game.team_count):
            for i2 in range(the_game.teams[i].player_count):
                the_game.teams[i].total_negative += the_game.teams[i].players[i2].negative
                total_positive += the_game.teams[i].players[i2].positive

    # Find the lower and upper ranges for both negative and positive
    for i in range(the_game.team_count):
            for i2 in range(the_game.teams[i].player_count):
                the_game.teams[i].players[i2].lower_negative_range = negative_upper
                the_game.teams[i].players[i2].upper_negative_range = the_game.teams[i].players[i2].negative / the_game.teams[i].total_negative
                negative_upper = numpy.nextafter(the_game.teams[i].players[i2].upper_negative_range, 1)
                the_game.teams[i].players[i2].lower_positive_range = positive_upper
                the_game.teams[i].players[i2].upper_positive_range = the_game.teams[i].players[i2].positive / total_positive
                positive_upper = numpy.nextafter(the_game.teams[i].players[i2].upper_positive_range, 1)

def print_all_player_stats():
    for i in range(the_game.team_count):
            for i2 in range(the_game.teams[i].player_count):
                print('Team ' + str(i) + ' Player ' + str(i2) + ' Name: ' + the_game.teams[i].players[i2].name)
                print('Team ' + str(i) + ' Player ' + str(i2) + ' Kills: ' + str(the_game.teams[i].players[i2].kills))
                print('Team ' + str(i) + ' Player ' + str(i2) + ' Deaths: ' + str(the_game.teams[i].players[i2].deaths))
                print('Team ' + str(i) + ' Player ' + str(i2) + ' KDR: ' + str(the_game.teams[i].players[i2].kdr))
                print('Team ' + str(i) + ' Player ' + str(i2) + ' DKR: ' + str(the_game.teams[i].players[i2].dkr))
                print('Team ' + str(i) + ' Player ' + str(i2) + ' KPR: ' + str(the_game.teams[i].players[i2].kpr))
                print('Team ' + str(i) + ' Player ' + str(i2) + ' DPR: ' + str(the_game.teams[i].players[i2].dpr))
                print('Team ' + str(i) + ' Player ' + str(i2) + ' HLTV Rating: ' + str(the_game.teams[i].players[i2].hltv_rating))
                print('Team ' + str(i) + ' Player ' + str(i2) + ' Inverse HLTV Rating: ' + str(the_game.teams[i].players[i2].inv_hltv_rating))
                print('Team ' + str(i) + ' Player ' + str(i2) + ' URL: ' + the_game.teams[i].players[i2].url)
                print('Team ' + str(i) + ' Player ' + str(i2) + ' Detailed URL: ' + the_game.teams[i].players[i2].stats_url)
                print('Team ' + str(i) + ' Player ' + str(i2) + ' Negative: ' + str(the_game.teams[i].players[i2].negative))
                print('Team ' + str(i) + ' Player ' + str(i2) + ' Positive: ' + str(the_game.teams[i].players[i2].positive))
                print('Team ' + str(i) + ' Player ' + str(i2) + ' Lower Negative Range: ' + str(the_game.teams[i].players[i2].lower_negative_range))
                print('Team ' + str(i) + ' Player ' + str(i2) + ' Upper Negative Range: ' + str(the_game.teams[i].players[i2].upper_negative_range))
                print('Team ' + str(i) + ' Player ' + str(i2) + ' Lower Positive Range: ' + str(the_game.teams[i].players[i2].lower_positive_range))
                print('Team ' + str(i) + ' Player ' + str(i2) + ' Upper Positive Range: ' + str(the_game.teams[i].players[i2].upper_positive_range))
                print('Team ' + str(i) + ' Player ' + str(i2) + ' Alive: ' + str(the_game.teams[i].players[i2].alive))
                print()
                

simulations = 3 # Go through kdr, kpr, and hltv_rating simulations
for current_simulation in range(simulations):
    print('Current Simulation: ' + str(current_simulation))
    if (current_simulation == 0):
        for i in range(the_game.team_count):
            for i2 in range(the_game.teams[i].player_count):
                the_game.teams[i].players[i2].negative = the_game.teams[i].players[i2].dkr
                the_game.teams[i].players[i2].positive = the_game.teams[i].players[i2].kdr
    elif (current_simulation == 1):
        for i in range(the_game.team_count):
            for i2 in range(the_game.teams[i].player_count):
                the_game.teams[i].players[i2].negative = the_game.teams[i].players[i2].dpr
                the_game.teams[i].players[i2].positive = the_game.teams[i].players[i2].kpr
    elif (current_simulation == 2):
        for i in range(the_game.team_count):
            for i2 in range(the_game.teams[i].player_count):
                the_game.teams[i].players[i2].negative = the_game.teams[i].players[i2].inv_hltv_rating
                the_game.teams[i].players[i2].positive = the_game.teams[i].players[i2].hltv_rating

    print()
    print_all_player_stats()
    '''            
    trials = 10000
    # Top level trials
    for current_trial in trials:
        
        # Top level bestof
        for current_bestof in range(floor(0.5 * the_game.bestof) + 1):
            
            # Current round wins
            for current_round in range(floor(0.5 * the_game.rounds) + 1):
                if((the_game.teams[0].won_rounds == floor(0.5 the_game.rounds)) and (the_game.teams[1].won_rounds == floor(0.5 the_game.rounds))): # Hard coded for two teams but I don't care
                    the_game.rounds += 10
    ''' 
