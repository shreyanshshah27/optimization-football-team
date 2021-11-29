!pip install pulp
import pulp
import numpy as np
import pandas as pd
import re

players_data = pd.read_csv(
    "https://raw.githubusercontent.com/shreyanshshah27/optimization-football-team/master/cleaned_players.csv"
)

players_data['player_position']=''
for index, data in players_data.iterrows():
  if(data['element_type']==1):
    players_data.loc[index,"player_position"]="GK"
  elif(data['element_type']==2):
    players_data.loc[index,"player_position"]="DEF"
  elif(data['element_type']==3):
    players_data.loc[index,"player_position"]="MID"
  else:
    players_data.loc[index,"player_position"]="FWD"
players_data['full_name'] = players_data.first_name + " " + players_data.second_name

available_cash=1000

prob = pulp.LpProblem('FootballOptimization', pulp.LpMaximize)

decision_variables = []
for index in range(len(players_data)):
    variable = str('x' + str(index))
    variable = pulp.LpVariable(str(variable), lowBound = 0, upBound = 1, cat= 'Integer')
    decision_variables.append(variable)

print ("Total number of decision_variables: " + str(len(decision_variables)))

total_points = ""
for index, data in players_data.iterrows():
    for i, player in enumerate(decision_variables):
        if index == i:
            formula = data['total_points']*player
            total_points += formula

prob += total_points

total_paid = ""
for index, data in players_data.iterrows():
    for i, player in enumerate(decision_variables):
        if index == i:
            formula = data['now_cost']*player
            total_paid += formula

prob += (total_paid <= available_cash)

required_gk = 2
selected_gk = ""
for index, data in players_data.iterrows():
    for i, player in enumerate(decision_variables):
        if index == i:
            if data['player_position'] == "GK":
                formula = 1*player
                selected_gk += formula

prob += (selected_gk == required_gk)

required_def = 5
selected_def = ""
for index, data in players_data.iterrows():
    for i, player in enumerate(decision_variables):
        if index == i:
            if data['player_position'] == "DEF":
                formula = 1*player
                selected_def += formula

prob += (selected_def == required_def)

required_mid = 5
selected_mid = ""
for index, data in players_data.iterrows():
    for i, player in enumerate(decision_variables):
        if index == i:
            if data['player_position'] == "MID":
                formula = 1*player
                selected_mid += formula

prob += (selected_mid == required_mid)

required_fwd = 3
selected_fwd = ""
for index, data in players_data.iterrows():
    for i, player in enumerate(decision_variables):
        if index == i:
            if data['player_position'] == "FWD":
                formula = 1*player
                selected_fwd += formula

prob += (selected_fwd == required_fwd)

team_dict= {}
for team in set(players_data.team_code):
    team_dict[str(team)]=dict()
    team_dict[str(team)]['avail'] = 3
    team_dict[str(team)]['total'] = ""
    for index, data in players_data.iterrows():
        for i, player in enumerate(decision_variables):
            if index == i:
                if data['team_code'] == team:
                    formula = 1*player
                    team_dict[str(team)]['total'] += formula

    prob += (team_dict[str(team)]['total'] <= team_dict[str(team)]['avail'])

prob.writeLP('FootballOptimization.lp')
optimization_result = prob.solve()

assert optimization_result == pulp.LpStatusOptimal
print("Status:", pulp.LpStatus[prob.status])
print("Optimal Solution to the problem: ", pulp.value(prob.objective))
print ("Individual decision_variables: ")
for v in prob.variables():
  if(v.varValue==1):
  	print(v.name, "=", v.varValue)

finalindex=[]
for v in prob.variables():
  if(v.varValue==1):
    rowindex=int(v.name[1:4])
    finalindex.append(rowindex)
df3=players_data.iloc[finalindex]

total_cost=0
expected_points=0
print("Selected players in the final team:")
for index, data in df3.iterrows():
  print(data["first_name"]+ " " +data["second_name"])
for index, data in df3.iterrows():
  total_cost=total_cost+data["now_cost"]
  expected_points+=data["total_points"]
print("Total cost=",total_cost)
print("Expected Points=",expected_points)
