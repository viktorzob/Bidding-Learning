# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 15:42:44 2020

@author: Viktor
"""

import numpy as np
import gym
from collections import deque
import random

# Ornstein-Ulhenbeck Process
# Taken from #https://github.com/vitchyr/rlkit/blob/master/rlkit/exploration_strategies/ou_strategy.py
# starting max_sigma = 0.3
class OUNoise(object):
    def __init__(self, action_space, mu=0.0, theta=0.15, max_sigma=0.3, min_sigma=0.3, decay_period=100000, discrete = 0, discrete_split = 0):
        self.mu           = mu
        self.theta        = theta
        self.sigma        = max_sigma
        self.max_sigma    = max_sigma
        self.min_sigma    = min_sigma
        self.decay_period = decay_period
        ##############
        #BiddingMarket_energy_Environment Params
        self.discrete = discrete
        self.discrete_split = discrete_split
        if discrete == 1:
            self.action_dim   = 1
            self.low          = 0
            self.high         = 10000
            if self.discrete_split == 1:
                self.action_dim   = 3
        else:      
            self.action_dim   = action_space.shape[0]
            self.low          = action_space.low
            self.high         = action_space.high
        ##################
        self.reset()
        
    def reset(self):
        self.state = np.ones(self.action_dim) * self.mu
        
    def evolve_state(self):
        x  = self.state
        dx = self.theta * (self.mu - x) + self.sigma * np.random.randn(self.action_dim) 
        # np.random.randn(0)
        #dx = self.theta * (self.mu - x) + self.sigma * (np.random.randn(self.action_dim) * 7)
        self.state = x + dx
        return self.state
    
    def get_action(self, action, t=0):
        ou_state = self.evolve_state()
        self.sigma = self.max_sigma - (self.max_sigma - self.min_sigma) * min(1.0, t / self.decay_period)
        return np.clip(action + ou_state, self.low, self.high)


# https://github.com/openai/gym/blob/master/gym/core.py
class NormalizedEnv(gym.ActionWrapper):   ## fehlt evtl. was
    """ Wrap action """

    def _action(self, action):
        act_k = (self.action_space.high - self.action_space.low)/ 2.
        act_b = (self.action_space.high + self.action_space.low)/ 2.
        return act_k * action + act_b

    def _reverse_action(self, action):
        act_k_inv = 2./(self.action_space.high - self.action_space.low)
        act_b = (self.action_space.high + self.action_space.low)/ 2.
        return act_k_inv * (action - act_b)
        

class Memory:
    def __init__(self, max_size):
        self.max_size = max_size
        self.buffer = deque(maxlen=max_size)
    
    def push(self, state, action, reward, next_state, done):
        
        #experience = (state, action, np.array([reward]), next_state, done) ### rewards haben bei mir sonst zu viele dimensionen
        experience = (state, action, reward, next_state, done)
        self.buffer.append(experience)

    def sample(self, batch_size):
        state_batch = []
        action_batch = []
        reward_batch = []
        next_state_batch = []
        done_batch = []

        batch = random.sample(self.buffer, batch_size)

        for experience in batch:
            state, action, reward, next_state, done = experience
            state_batch.append(state)
            action_batch.append(action)
            reward_batch.append(reward)
            next_state_batch.append(next_state)
            done_batch.append(done)
        
        return state_batch, action_batch, reward_batch, next_state_batch, done_batch

    def __len__(self):
        return len(self.buffer)




class GaussianNoise(object):
    def __init__(self, action_space, mu = 0.0, sigma = 0.1, regulation_coef = 1, decay_rate = 0.1):
        
        self.action_dim      = action_space.shape[0]
        self.low             = action_space.low
        self.high            = action_space.high
        self.distance        = abs(self.low - self.high)
        
        self.decay_rate = decay_rate 
        self.regulation_coef = regulation_coef
        self.mu              = mu
        self.sigma           = sigma
        
        self.reset()
        
        
    def reset(self):
        self.state = np.ones(self.action_dim) * self.mu
    

    def get_action(self, action, step = 0):
         
        noise_list = np.random.normal(self.mu, self.sigma, self.action_dim)* (self.distance *self.regulation_coef)
        noise_list = noise_list *(1 - self.decay_rate)**step
        
        noisy_action = np.clip(action + noise_list, self.low, self.high)

        return noisy_action 
    
    

      