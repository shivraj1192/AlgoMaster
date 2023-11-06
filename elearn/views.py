
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import TransportationForm
import numpy as np




# Create your views here.

def home(request):
    return render(request,'home.html')




def north_west_method(request):
    if request.method == 'POST':
        form = TransportationForm(request.POST)
        if form.is_valid():
            # Process the form data here
            supply = np.array(form.cleaned_data['supply'].split(), dtype=int)
            demand = np.array(form.cleaned_data['demand'].split(), dtype=int)
            cost_matrix = []

            for row in form.cleaned_data['cost_matrix'].split('\n'):
                cost_matrix.append(list(map(int, row.split())))

            cost_matrix = np.array(cost_matrix)

            if np.sum(supply) != np.sum(demand):
                return render(request, 'north_west_method.html', {'form': form, 'error_message': 'Supply and demand are not balanced.'})

            if cost_matrix.shape != (len(supply), len(demand)):
                return render(request, 'north_west_method.html', {'form': form, 'error_message': 'Cost matrix does not match supply and demand dimensions.'})


            # Perform transportation problem solving here
            allocation = np.zeros((len(supply), len(demand)))

            i, j = 0, 0  # Start from the top-left corner
            while i < len(supply) and j < len(demand):
                min_supply_demand = min(supply[i], demand[j])

                allocation[i][j] = min_supply_demand

                supply[i] -= min_supply_demand
                demand[j] -= min_supply_demand

                if supply[i] == 0:
                    i += 1
                else:
                    j += 1

            total_cost = np.sum(allocation * cost_matrix)

            return render(request, 'results.html', {
                'supply': form.cleaned_data['supply'],
                'demand': form.cleaned_data['demand'],
                'cost_matrix': cost_matrix.tolist(),  # Pass the cost_matrix variable as a list
                'allocation_matrix': allocation.tolist(),
                'total_cost': total_cost,
            })

    else:
        form = TransportationForm()

    return render(request, 'north_west_method.html', {'form': form})










def least_cost_method(request):
    if request.method == 'POST':
        form = TransportationForm(request.POST)
        if form.is_valid():
            # Process the form data here
            supply = np.array(form.cleaned_data['supply'].split(), dtype=int)
            demand = np.array(form.cleaned_data['demand'].split(), dtype=int)
            cost_matrix = []

            for row in form.cleaned_data['cost_matrix'].split('\n'):
                cost_matrix.append(list(map(int, row.split())))

            cost_matrix = np.array(cost_matrix)

            # Check if supply and demand are balanced
            if np.sum(supply) != np.sum(demand):
                return render(request, 'least_cost_method.html', {'form': form, 'error_message': 'Supply and demand are not balanced.'})
            if cost_matrix.shape != (len(supply), len(demand)):
                return render(request, 'least_cost_method.html', {'form': form, 'error_message': 'Cost matrix does not match supply and demand dimensions.'})

            # Perform least cost method here
            allocation = np.zeros((len(supply), len(demand)))
            dummy = cost_matrix.copy()  # Create a copy of cost_matrix

            while np.sum(supply) > 0 and np.sum(demand) > 0:
                min_cost = np.min(cost_matrix)
                min_cost_indices = np.argwhere(cost_matrix == min_cost)
                i, j = min_cost_indices[0]

                allocation[i][j] = min(supply[i], demand[j])

                supply[i] -= allocation[i][j]
                demand[j] -= allocation[i][j]

                cost_matrix[i, j] = 999999  # Mark as visited with infinity

            # Calculate the total_cost using the dummy matrix
            total_cost = 0
            print(dummy ,"and",total_cost)
            for i in range(len(supply)):
                for j in range(len(demand)):
                    total_cost += allocation[i][j] * dummy[i][j]
                    print(allocation[i][j])
                    print(dummy[i][j])
                    print(total_cost)

            return render(request, 'results.html', {
                'supply': form.cleaned_data['supply'],
                'demand': form.cleaned_data['demand'],
                'cost_matrix': dummy.tolist(),
                'allocation_matrix': allocation.tolist(),
                'total_cost': total_cost,
            })
    else:
        form = TransportationForm()

    return render(request, 'least_cost_form.html', {'form': form})







def row_minima_method(request):
    if request.method == 'POST':
        form = TransportationForm(request.POST)
        if form.is_valid():
            # Process the form data here
            supply = np.array(form.cleaned_data['supply'].split(), dtype=int)
            demand = np.array(form.cleaned_data['demand'].split(), dtype=int)
            cost_matrix = []

            for row in form.cleaned_data['cost_matrix'].split('\n'):
                cost_matrix.append(list(map(int, row.split())))

            cost_matrix = np.array(cost_matrix)

            # Check if supply and demand are balanced
            if np.sum(supply) != np.sum(demand):
                return render(request, 'row_minima_method.html', {'form': form, 'error_message': 'Supply and demand are not balanced.'})

            if cost_matrix.shape != (len(supply), len(demand)):
                return render(request, 'row_minima_method.html', {'form': form, 'error_message': 'Cost matrix does not match supply and demand dimensions.'})

            # Perform Row Minima Method here
            allocation = np.zeros((len(supply), len(demand)))
            dummy = cost_matrix.copy()  # Create a copy of cost_matrix
            i = 0
            while i < len(supply):
                row_minima = np.min(cost_matrix, axis=1)
                
                if supply[i] == 0:
                    i += 1
                    continue

                min_cost_row = i
                min_cost = row_minima[min_cost_row]
                if np.all(demand == 0):
                    break
                col_index = np.argmin(cost_matrix[min_cost_row])
                

                allocation[min_cost_row][col_index] = min(supply[min_cost_row], demand[col_index])

                supply[min_cost_row] -= allocation[min_cost_row][col_index]
                demand[col_index] -= allocation[min_cost_row][col_index]

                # Replace np.inf with a big number (e.g., 999999)
                cost_matrix[min_cost_row][col_index] = 999999
                print(cost_matrix)
                print(allocation)
                print(supply)
                print(demand)


            # Calculate the total_cost using the dummy matrix
            total_cost = 0
            for i in range(len(supply)):
                for j in range(len(demand)):
                    total_cost += allocation[i][j] * dummy[i][j]
            
            print(total_cost)

            return render(request, 'results.html', {
                'supply': form.cleaned_data['supply'],
                'demand': form.cleaned_data['demand'],
                'cost_matrix': dummy.tolist(),
                'allocation_matrix': allocation.tolist(),
                'total_cost': total_cost,
            })
    else:
        form = TransportationForm()
    
    

    return render(request, 'row_minima_method.html', {'form': form})




def column_minima_method(request):
    if request.method == 'POST':
        form = TransportationForm(request.POST)
        if form.is_valid():
            # Process the form data here
            supply = np.array(form.cleaned_data['supply'].split(), dtype=int)
            demand = np.array(form.cleaned_data['demand'].split(), dtype=int)
            cost_matrix = []

            for row in form.cleaned_data['cost_matrix'].split('\n'):
                cost_matrix.append(list(map(int, row.split())))

            cost_matrix = np.array(cost_matrix)

            # Check if supply and demand are balanced
            if np.sum(supply) != np.sum(demand):
                return render(request, 'column_minima_method.html', {'form': form, 'error_message': 'Supply and demand are not balanced.'})

            if cost_matrix.shape != (len(supply), len(demand)):
                return render(request, 'column_minima_method.html', {'form': form, 'error_message': 'Cost matrix does not match supply and demand dimensions.'})

            # Perform Column Minima Method here
            allocation = np.zeros((len(supply), len(demand)))
            dummy = cost_matrix.copy()  # Create a copy of cost_matrix
            j = 0
            while j < len(demand):
                col_minima = np.min(cost_matrix, axis=0)

                if demand[j] == 0:
                    j += 1
                    continue

                min_cost_col = j
                min_cost = col_minima[min_cost_col]
                if np.all(supply == 0):
                    break
                row_index = np.argmin(cost_matrix[:, min_cost_col])

                allocation[row_index][min_cost_col] = min(supply[row_index], demand[min_cost_col])

                supply[row_index] -= allocation[row_index][min_cost_col]
                demand[min_cost_col] -= allocation[row_index][min_cost_col]

                # Replace np.inf with a big number (e.g., 999999)
                cost_matrix[row_index][min_cost_col] = 999999
                print(cost_matrix)
                print(allocation)
                print(supply)
                print(demand)

            # Calculate the total_cost using the dummy matrix
            total_cost = 0
            for i in range(len(supply)):
                for j in range(len(demand)):
                    total_cost += allocation[i][j] * dummy[i][j]

            print(total_cost)

            return render(request, 'results.html', {
                'supply': form.cleaned_data['supply'],
                'demand': form.cleaned_data['demand'],
                'cost_matrix': dummy.tolist(),
                'allocation_matrix': allocation.tolist(),
                'total_cost': total_cost,
            })
    else:
        form = TransportationForm()

    return render(request, 'column_minima_method.html', {'form': form})


import numpy as np

def vogels_approximation_method(request):
    if request.method == 'POST':
        form = TransportationForm(request.POST)
        if form.is_valid():
            # Process the form data here
            supply = np.array(form.cleaned_data['supply'].split(), dtype=int)
            demand = np.array(form.cleaned_data['demand'].split(), dtype=int)
            cost_matrix = []

            for row in form.cleaned_data['cost_matrix'].split('\n'):
                cost_matrix.append(list(map(int, row.split())))

            cost_matrix = np.array(cost_matrix)

            # Check if supply and demand are balanced
            if np.sum(supply) != np.sum(demand):
                return render(request, 'vogels_approximation_method.html', {'form': form, 'error_message': 'Supply and demand are not balanced.'})

            if cost_matrix.shape != (len(supply), len(demand)):
                return render(request, 'vogels_approximation_method.html', {'form': form, 'error_message': 'Cost matrix does not match supply and demand dimensions.'})

            
            # Perform Vogel's Approximation Method here
            allocation = np.zeros((len(supply), len(demand)))
            dummy = cost_matrix.copy()  # Create a copy of cost_matrix

            while np.sum(supply) > 0 and np.sum(demand) > 0:
                row_penalties = np.zeros(len(supply))
                col_penalties = np.zeros(len(demand))

                for i in range(len(supply)):
                    if supply[i] > 0:
                        min1 = min(cost_matrix[i, :])
                        min2 = min(cost_matrix[i, :][cost_matrix[i, :] != min1])
                        row_penalties[i] = min2 - min1

                for j in range(len(demand)):
                    if demand[j] > 0:
                        min1 = min(cost_matrix[:, j])
                        min2 = min(cost_matrix[:, j][cost_matrix[:, j] != min1])
                        col_penalties[j] = min2 - min1

                max_row_penalty_idx = np.argmax(row_penalties)
                max_col_penalty_idx = np.argmax(col_penalties)
                # print(max_row_penalty_idx,"row penal   and value",row_penalties[max_row_penalty_idx])
                # print(max_col_penalty_idx,"col penal   and value",col_penalties[max_col_penalty_idx])
                

                if row_penalties[max_row_penalty_idx] >= col_penalties[max_col_penalty_idx]:
                    # Allocate from the row with the highest penalty
                    row_index = max_row_penalty_idx
                    col_index = np.argmin(cost_matrix[row_index])
                else:
                    # Allocate from the column with the highest penalty
                    col_index = max_col_penalty_idx
                    row_index = np.argmin(cost_matrix[:, col_index])

                # print("Row index:", row_index)
                # print("Column index:", col_index)

                # Calculate the minimum supply to allocate
                min_supply = min(supply[row_index], demand[col_index])
                # print("Min supply:", min_supply)
                # print("############gap#################")

                # Perform allocation, update supply and demand
                allocation[row_index][col_index] = min_supply
                supply[row_index] -= min_supply
                demand[col_index] -= min_supply

                cost_matrix[row_index][col_index] = 999999  # Mark as allocated
                if supply[row_index] == 0:
                    # Set all elements in the row to 999999
                    cost_matrix[row_index, :] = 999999

                if demand[col_index] == 0:
                    # Set all elements in the column to 999999
                    cost_matrix[:, col_index] = 999999
                # print(supply,demand,cost_matrix)

            # Calculate the total_cost using the dummy matrix
            total_cost = np.sum(allocation * dummy)

            return render(request, 'results.html', {
                'supply': form.cleaned_data['supply'],
                'demand': form.cleaned_data['demand'],
                'cost_matrix': dummy.tolist(),
                'allocation_matrix': allocation.tolist(),
                'total_cost': total_cost,
            })
    else:
        form = TransportationForm()

    return render(request, 'vogels_approximation_method.html', {'form': form})

