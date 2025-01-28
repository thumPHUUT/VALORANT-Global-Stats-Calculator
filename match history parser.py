import json
from datetime import datetime

file_path = 'D:/Python/valorant_match_history.json' #change this to reflect your json location
with open(file_path, "r") as file:
    data = json.load(file)
file.close()


def delta_time_seconds(t1, t2):
    t1UTC = datetime.strptime(t1, "%Y-%m-%d %H:%M:%S")
    t2UTC = datetime.strptime(t2, "%Y-%m-%d %H:%M:%S")
    delta_t = t1UTC - t2UTC

    return delta_t.total_seconds()

def validate_year(year_list, utc_input):
    utc_date = datetime.strptime(utc_input, "%Y-%m-%d %H:%M:%S")
    input_year = utc_date.year

    return input_year in year_list

def print_data(data, year):
    #year condition will output statistics for set year. setting to None will print stats for all years
    ranked_playtime, playtime, num_wins_ranked, num_losses_ranked, num_wins, num_losses, num_losses_dm, num_wins_dm= [0]*8
    win_rate_ranked, win_rate, win_rate_w_dm = [0.0] * 3
    dm_condition, ranked_condition = [False] * 2
    
    if year != None: 
        year_list = [year]
    else:
        year_list = [2020, 2021, 2022, 2023, 2024] #this will need to be updated to include more years if I do this again

    for dict in data:
        if validate_year(year_list, dict["game_start_time_utc"]):
            playtime += delta_time_seconds( dict["game_end_time_utc"], dict["game_start_time_utc"] )
            if dict["game_type"] == "Ranked":
                ranked_playtime += delta_time_seconds( dict["game_end_time_utc"], dict["game_start_time_utc"] )
                ranked_condition = True
            if dict["game_type"] == "Deathmatch": 
                dm_condition = True
            if dict["game_mode"] == "Matchmaking":
                if dict["game_outcome"] == "Win":
                    num_wins += 1
                    if dm_condition: num_wins_dm += 1
                    if ranked_condition: num_wins_ranked += 1
                else:
                    num_losses += 1
                    if dm_condition: num_losses_dm += 1
                    if ranked_condition: num_losses_ranked += 1

            dm_condition = False
            ranked_condition = False

    ranked_playtime_hours = ranked_playtime / 3600
    playtime_hours = playtime / 3600

    win_rate_ranked = num_wins_ranked / (num_wins_ranked + num_losses_ranked)
    win_rate_w_dm = num_wins / (num_wins + num_losses)
    win_rate = ( num_wins - num_wins_dm) / (num_wins + num_losses - num_wins_dm - num_losses_dm)

    if year == None: 
        print("\nLifetime statistics:\n")
    else:
        print("\n{} statistics\n".format(year))

    print("games played (including deathmatch)          : ", num_wins+num_losses)
    print("games played (excluding deathmatch)          : ", num_wins+num_losses- num_wins_dm - num_losses_dm)
    print("Ranked games played                          : ", num_losses_ranked + num_wins_ranked)

    print("all modes winrate (excluding deathmatch)     : ", round(win_rate, 3))
    print("all modes winrate (including deathmatch)     : ", round(win_rate_w_dm, 3))
    print("Ranked winrate                               : ", round(win_rate_ranked, 3) )

    print("Total ranked playtime (hours)                : ", round(ranked_playtime_hours, 1))
    print("Total playtime all modes (hours)             : ", round(playtime_hours, 1))

print_data(data, None)
print_data(data, 2024)
#print_data(data, 2023)
#print_data(data, 2022)
#print_data(data, 2021)
#print_data(data, 2020)