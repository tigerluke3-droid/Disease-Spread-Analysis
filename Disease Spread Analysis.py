'''
CS 111 Project 4
Tracking the Spread of Disease 
3/9/2026
Names: <Johnathan Zheng and Luke McMiller>

This program uses the random python module and SIR model of disease spread to demonstrate how different 
variations in terms of population size, trasmission rates, etc. can effect how many people end up being
infected from a disease, as well as how many people can recover from a disease when there is randomness versus
no randomness.

'''
#Moduls imported for project
import random
import matplotlib.pyplot as plt

#The following code is meant to present the expected trajectory of an epidemic, if there was no randomness involved.
def expectedTrajectory(population, transmissionrate, recoveryrate):
    
    i = 1.0
    s = population - i
    r = 0.0

    day = 0.0
    peak_day = day
    peak_i = i

    i_list = [i]
    s_list = [s]
    r_list = [r]
    days = [0]
    while i >= 1:
        new_infectious = transmissionrate * s * i / population
        new_recovered = recoveryrate * i

        s = s - new_infectious
        i = i + new_infectious - new_recovered
        r = r + new_recovered

        day += 1
        if i > peak_i:
            peak_i = i
            peak_day = day
        i_list.append(i)
        s_list.append(s)
        r_list.append(r)
        days.append(day)

    neversick = s
    herdday = day
    print('Peak of' , round(peak_i) , 'infectious people reached after' , round(peak_day) , 'days.')
    print('Herd immunity reached after' , round(herdday) , 'days with' , round(r) , 'people who '
    'recovered and' , round(neversick) , 'people who never got sick')
    return round(peak_i), round(peak_day), round(herdday), round(r), round(neversick), i_list, s_list, r_list, days

#The following is code that showcases a graph of based on the information from the expected expectedTrajectory function.
def plotTrajectory(i_list, s_list, r_list, days):
    plt.plot(days, s_list, label="Susceptible (S)")
    plt.plot(days, i_list, label="Infectious (I)")
    plt.plot(days, r_list, label="Recovered (R)")
    plt.xlabel("Days")
    plt.ylabel("People")
    plt.title("SIR Simulation")
    plt.legend()
    plt.show()

#The following is code that is meant to present how many infected people are able to recover based off a given recovery rate.
def infectiousToRecovered(infectious, recoveryRate):
    recoveredPeople = 0
    for i in range(1, infectious + 1):
        recoveredValue = random.random()
        if recoveredValue < recoveryRate:
            recoveredPeople = recoveredPeople + 1
    
    return recoveredPeople

#The following is code that is meant to present how many new infected people there will be if susceptible individuals came into contact with an infected person.
def susceptibleToInfectious(susceptible, infectiousPeople, population, transmissionRate, infectiousContact):
    contactSusceptible = susceptible/population
    susceptibleCInfections = transmissionRate/ infectiousContact

    newInfectiousPeople = 0
    for i in range(1, infectiousPeople + 1): # Goes through each infected person
        for x in range(1, infectiousContact + 1):
            if random.random() < contactSusceptible:
                if random.random() < susceptibleCInfections:
                    newInfectiousPeople = newInfectiousPeople + 1
    
    return newInfectiousPeople

#The following code is meant to present the Monte Carlo Trajecotry of an epidemic, if there was randomness involved.
def monteCarloTrajectory(population, transmissionrate, recoveryrate, infectiousContact):
    i = 1
    s = population - 1
    r = 0

    day = 0
    peak_day = 0
    peak_i = i

    while i >= 1:
        new_infectious = susceptibleToInfectious(s, i, population, transmissionrate, infectiousContact)
        new_recovered = infectiousToRecovered(i, recoveryrate)

        if new_infectious > s:
            new_infectious = s

        s = s - new_infectious
        i = i + new_infectious - new_recovered
        r = r + new_recovered

        day += 1
        if i > peak_i:
            peak_i = i
            peak_day = day

    neversick = s
    herdday = day
    print('Peak of', round(peak_i), 'infectious people reached after', round(peak_day), 'days.')
    print('Herd immunity reached after', round(herdday), 'days with', round(r), 'people who recovered and', round(neversick), 'people who never got sick')
    return round(peak_i)

def main():
    #Part 1
    peak_i, peak_day, herdday, r_end, s_end, i_list, s_list, r_list, days = expectedTrajectory(100, 0.3, 1/14)
    plotTrajectory(i_list, s_list, r_list, days)

    #Part 2
    for x in range(5):
        print (susceptibleToInfectious(46, 17, 100, 0.3, 10), x) 
        print (infectiousToRecovered(17, 1/7), x) 
    
    #Part 3

    total_peak = 0
    for i in range(100):
        total_peak = total_peak + monteCarloTrajectory(100, 0.3, 1/14, 20)
    average_peak = total_peak / 100
    print("Average Monte Carlo peak:", round(average_peak))


main()