# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 21:52:11 2020

@author: Gurpinder
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

# CHANGE THE NAME OF THE FILE AND WEBDRIVER PATH HERE !!
file_name = "test.fasta" 
driver_path = r"C:\Users\Gurpi\gecko-firefox\geckodriver.exe" #don't know the funtion of "r", if the driver is a system PATH variable, no need for full path ofcourse. 


def reader(path):
    """
    Reads a file containing multiple fasta sequences and outputs them as a dictionary
    input:
        path: file path to open
    returns:
        seqs: a dictionary with sequence name and sequence itself as key, value pairs.
    """
    seqs = {}
    with open(path, "r") as f:
        Lines = f.readlines()
        for line in Lines:
            if line.startswith(">"):
                accession = line.split(" ")[0][1:]
                seq = ""
            else:
                seq = seq + line.replace("\n","")
            seqs[accession] = seq
    return seqs


def AllerTOP(driver, sequence_string, sequence_meta=None):
    """
    Uses selenium webdriver to get Allergen/Non-Allergen information from AllerTOPv2.
    
    input:
        driver: any selenium webdriver object (tested with geckodriver)
        sequence_string: protein to test
        sequence_meta(optional): name of the sequence
    """
    
    print("Connecting to AllerTOP..")
    driver.get("http://www.ddg-pharmfac.net/AllerTOP/")
    print("Connected to AllerTOP.")
    text_box = driver.find_element_by_xpath('//*[@id="sequence"]') #Xpath for text box
    text_box.send_keys(sequence_string) #paste the sequence
    
    #press the submit button
    driver.find_element_by_xpath('/html/body/center/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr/td/form/table/tbody/tr[3]/td/input').click()

    time.sleep(3) #time for the server to calculate the results and refresh the page.
    result = driver.find_element_by_xpath('/html/body/center/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr/td/form/table/tbody/tr/td/div/h4[2]').text
    
    if sequence_meta:
        print("{} is {}".format(sequence_meta, result))
    return result                


with open("OUTPUT_"+file_name, "a") as out_f:                               
    
    start = time.time()
    
    opts = Options()
    opts.set_headless() #do not display the window, operate in headless mode
    driver = webdriver.Firefox(executable_path=driver_path, options=(opts))
    seqs = reader(file_name) #reading the file
    
    for seq in list(seqs.keys()):
        protein = seqs[seq]
        result = AllerTOP(driver, protein, seq)
        out_f.write(seq+","+result+"\n")
        time.sleep(3) #3 second time between proteins.
    driver.close()
    
    end = time.time()

    print("Done")
    print("Time_taken: {}s".format(round(end-start, 3))) #average 9 seconds per protein (6 seconds wait time)
