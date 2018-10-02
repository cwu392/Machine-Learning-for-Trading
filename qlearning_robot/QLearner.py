"""
Template for implementing QLearner  (c) 2015 Tucker Balch
"""

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.s = 0
        self.a = 0
        self.rar=rar
        self.radr=radr
        self.gamma=gamma
        self.alpha=alpha
        self.dyna=dyna

        ###########
        self.Q_table=np.zeros((num_states,num_actions))
        self.Dyna_T=np.zeros((0, 4), dtype=int)

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        # self.s = s
        # action = rand.randint(0, self.num_actions-1)
        # self.a = action
        self.s=s
        if self.rar > rand.random():
            action = rand.randint(0, self.num_actions-1)
        else:
            action=np.argmax(self.Q_table[s,:])
        self.rar*=self.radr
        self.a=action
        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The new state
        @returns: The selected action
        """
        #action = rand.randint(0, self.num_actions-1)
        self.Q_table[self.s,self.a]=(1-self.alpha)*self.Q_table[self.s,self.a]+self.alpha*(r+self.gamma*max(self.Q_table[s_prime,:]))
        
        if self.dyna >0:
            self.Dyna_T=np.r_[self.Dyna_T, np.array([[self.s,self.a,s_prime,r]])]
            random_index = np.random.choice(self.Dyna_T.shape[0],self.dyna,replace=True)
            dyna_s=self.Dyna_T[random_index,0]
            dyna_a=self.Dyna_T[random_index,1]
            dyna_s_prime=self.Dyna_T[random_index,2]
            dyna_r=self.Dyna_T[random_index,3]
            for i in range(len(dyna_s)):
                self.update_Q(dyna_s[i],dyna_a[i],dyna_s_prime[i],dyna_r[i])

        if self.rar > rand.uniform(0, 1):
            action = rand.randint(0, self.num_actions-1)
        else:
            action=np.argmax(self.Q_table[s_prime,:])
        self.rar*=self.radr
        self.a=action
        self.s=s_prime
        if self.verbose: print "s =", s_prime,"a =",action,"r =",r
        return action

    def update_Q(self,s,a,s_prime,r):
        self.Q_table[s,a]=(1-self.alpha)*self.Q_table[s,a]+self.alpha*(r+self.gamma*max(self.Q_table[s_prime,:])) 

        if self.rar > rand.uniform(0, 1):
            action = rand.randint(0, self.num_actions-1)
        else:
            action=np.argmax(self.Q_table[s_prime,:])
        return 
    def author(self):
        return 'cwu392'

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"