#imports
import matplotlib.pyplot as plt
import numpy as np

#class
class Election:
    def __init__(self, district_number: str, dem_votes: int, rep_votes: int):
        """
        Description of Function: Instance variables

        Parameters: 
        district_number: str, number of the district
        dem_votes: int, number of Democratic votes in the district
        rep_votes: int, number of Republican votes in the district

        Return: None
        """
        self.district = district_number
        self.dem_votes = dem_votes
        self.rep_votes = rep_votes

#new dictionary
election_results = {}

#opening data file
with open("C_1202/gerryman/1976-2020votes.txt", "r") as a_file:
    for line in a_file:
        data = line.strip().split(',')

        #variables
        current_year = data[0]
        current_state = data[1]

        #creating a new dictionary key for year 
        #and list  of district objects for each state
        if current_year not in election_results.keys():
            election_results[current_year] = {}
        if current_state not in election_results[current_year].keys():
            election_results[current_year][current_state] = []
        for i in range(2, len(data), 3):
            election_results[current_year][current_state].append(Election(data[i], float(data[i+1]), float(data[i+2])))

def report_efficiency_gap(districts:list[Election]) -> None:
    """
    Description of Function: Returns the number of districts, wasted Democratic votes, 
    wasted Republican votes, and efficiencty gap and favor

    Parameters: districts: list of Election objects for the state

    Return: None
    """
    #variables
    total = 0

    dem_wasted_votes = []
    rep_wasted_votes = []

    for district in districts:    
        #variables
        dem_waste = 0
        rep_waste = 0
        total_per_district = 0
        total_to_win = 0

        total_per_district = float(district.dem_votes) + float(district.rep_votes)
        total += total_per_district
        total_to_win = float(total_per_district) / 2
        
        #if the district was Democratic
        if district.dem_votes > district.rep_votes:
            dem_waste =dem_waste+ float(district.dem_votes) - total_to_win
            rep_waste =rep_waste+ float(district.rep_votes)

        #if the district was Republican
        elif district.dem_votes < district.rep_votes:
            rep_waste =rep_waste+ float(district.rep_votes) - total_to_win
            dem_waste =dem_waste+ float(district.dem_votes)

        dem_wasted_votes.append(dem_waste)
        rep_wasted_votes.append(rep_waste)

    ticks = []
    for i in range(1, len(districts) + 1):
        ticks.append(i)

    N = len(districts)
    ind = np.arange(N)

    dem = dem_wasted_votes
    rep = rep_wasted_votes

    p1 = plt.bar(ind, dem, color = 'b')
    p2 = plt.bar(ind, rep, color = 'r', bottom = dem)

    plt.ylabel('Number of Wasted Votes')
    plt.xlabel('District Number')
    plt.xticks(ind, ticks)
    plt.legend((p1[0], p2[0]), ('Democratic', 'Republican'))

    plt.savefig("election_results.jpg")
    plt.show()

def user_year() -> str:
    """
    Description of Function: Prompting the user for the election year
    Parameters: None
    Return: str
    """
    #variable
    year = input("What election year would you like to evaluate? ")

    #while loop to prompt again if the year is not valid
    while int(year) % 2 != 0 or int(year) < 1976 or int(year) > 2020:
        print("Sorry, valid election years are even years from 1976-2020.")
        year = input("What election year would you like to evaluate? ")
       
    return year

def user_state() -> str:
    """
    Description of Function:  Prompting the user for the election state
    Parameters: None
    Return: str
    """
    #variable
    state = input("What state would you like to evaluate? ")

    #while loop to prompt again if the state is not valid
    while state.upper() not in election_results[current_year].keys():
        print(f"{state} is not a valid state.")
        state = input("What state would you like to evaluate? ")

    return state.upper()

def evaluate_state()-> None:
    """
    Description of Function: Returns the efficiency gap for the year and state the user inputs
    Parameters: None
    Return: None
    """
    #variables
    year = user_year()
    state = user_state()

    plt.title(f'Wasted Votes in {state} in {year}')
    report_efficiency_gap(election_results[year][state])

#variables 
quit = False
continue_program = "yes"

#program description for user
print("This program evaluates districting fairness for US House elections from 1976-2020.")

#while loop
while not quit:
    #if the program is set to continue
    if continue_program == 'yes':
        evaluate_state()
        continue_program = input("Would you like to continue? ")
        continue_program = continue_program.lower()

    #if the the user wants to exit
    elif continue_program == 'no':
        quit = True

    #if the user response is not "yes" or "no"
    else:
        print("Invalid input. Try again.")
        continue_program = input("Would you like to continue? ")
