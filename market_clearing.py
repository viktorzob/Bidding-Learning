"""
Created on Wed Mar 18 18:03:36 2020

@author: Claude
"""
import numpy as np
import numpy_groupies as npg


#a = np.array([0,5,10])
#b = np.array([1,2,10])
#c = np.array([2,3,11])
#d = np.array([1,9,7])

#Flip
a = np.array([0,10, 2])
b = np.array([1,10,3])
c = np.array([2,11, 2])
d = np.array([1,7,9])


#Fringe Readout for Testing

#Readout fringe players from other.csv (m)
read_out = np.genfromtxt("others.csv",delimiter=";",autostrip=True,comments="#",skip_header=1,usecols=(0,1))
#Readout fringe switched to conform with format; finge[0]=quantity fringe[1]=bid
fringe = np.fliplr(read_out)
fringe = np.pad(fringe,((0,0),(1,0)),mode='constant')

#test_array = np.stack((a,b,d,a,b,c,b,c))
#test_array = np.stack((a,b,c))
test_array = fringe




demand =27


#print(test_array)
def market_clearing(demand,bids):    
    """ 
    Implements a uniform pricing market clearing of several players price-quantity bids
    Requires the bids in a certain from and numbered
    
    Input:
    -   demand as scalar
    -   Expects bids as an (3xn) Numpy Array
    1st Row Player Name, 2nd Row Quantity bid, 3rd Row Price-bid 
    
    Output:
    -   Market Price
    -   Ordered result of each quantity assigned by bid
    -   Assigns sold quantities per player
    
    #Attention: player labels need to be integers
    """
    
    # Sort by 3rd Row (ie by Price-Bids)
    ind = np.argsort(bids[:,2]) 
    bids = bids[ind]
    #print(bids)
    
    #Consecutively add up 2nd Row (ie Quantity-Bids)
    bids[:,1]=np.cumsum(bids[:,1])
    #print(bids)
    
    #Restrict Quantity by 0 and Demand
    bids[:,1]=np.clip(bids[:,1],0,demand)
    #print(bids)
    
    #Determine Position of Price setting player and Marketprice
    cutoff = np.argmax(bids[:,1])
    market_price = bids[cutoff,2]
    #print(bids)
    
    #Convert CumSum to Differences
    #This sets all quantities above cutoff to 0 and gives sold quantities below cutoff
    bids[:,1]=np.hstack((bids[0,1],np.diff(bids[:,1])))
    
    #print(bids)
    
    
    #Aggregate quantities py player name
    
    #Labels are player names in a[:,0] and Values are quantities in a[:,1]
    
    #Attention: the labels need to be integers
    #bids[:,0]=bids[:,0].astype(int)
    
    #Attention: without dtype float in the values we get an overflow
    
    quantities = npg.aggregate(bids[:,0].astype(int),bids[:,1],func='sum',dtype=np.float)
    
    return market_price, bids, quantities


market_clearing(7,test_array)


''' 
Possible Testcases:
    Check if sales \leq supply
    Check if sales \geq demand
    Check 3 cases low demand, equal demanl and high demand
'''



    