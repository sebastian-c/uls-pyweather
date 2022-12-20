# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 15:07:19 2022

@author: Sebastian
"""

class Presenter():
    def __init__(self, cont = False):
        self.cont = cont
        
    def pause(self, title="Objective"):
        
        if self.cont: 
            return None
        
        result = input("\n" + title + "\nPress any key to continue to the next question: (type 'skip' to avoid these halts')\n")
        
        if result == 'skip':
            self.cont = True
        return None

def KelvinToCelsius(kelvin):
    return(kelvin - 273.15)