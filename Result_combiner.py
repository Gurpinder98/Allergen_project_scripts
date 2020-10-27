# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 19:22:02 2020

@author: Gurpinder
"""
import os

CURRENT_DIR = os.getcwd()
FILES_DIR = str(input("Enter the name of the folder: "))
NAME_TO_BE_GIVEN = str(input("Name to be given to files: "))

file_list = os.listdir(FILES_DIR)

with open(NAME_TO_BE_GIVEN+"_combined.csv", "a") as combined:
     for file in file_list:
         with open(CURRENT_DIR+"\\"+ FILES_DIR + "\\" + file, "r") as input_file:
             print("Writing file {}.".format(file))
             lines = input_file.readlines()
             count = 0
             if count == 0:
                 combined.write(lines[0])
                 count = 1
             combined.write(''.join(lines[1:]))
