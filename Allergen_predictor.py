# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 18:48:31 2020

@author: Gurpinder
"""
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from selenium.webdriver.firefox.options import Options
import time
import requests
import random

import os
import sys

########################### Helper functions ##################################

def logging(file_name, action, message=None):
    """
    Simple logging utility for genome wide allergen prediction.

    Parameters
    ----------
    file_name : str
            Logging file name
    action : str
        "read" or "write"
    message : str, optional
        message to write. The default is None.

    Returns
    -------
    str
        last file name if OK
        -9 if any error occurs
    """
    
    if action == "read":
        
        log_file = open(file_name, "r")
        lines = log_file.readlines()
        log_file.close()
        if lines[-1].startswith("OK:"):
            return lines[-1].rstrip("\n")[3:]
        if lines[-1].startswith("ERROR:"):
            print("Last File status ERROR. Delete last file log in the log file.")
            return "-9"
        else:
            print("Problem in log file.")
            return "-9"
        
    if action == "write":
        with open(file_name, "a") as log_file:
            log_file.write(message + "\n")
            
            
def AllerCatPro(driver, file_path, file_name, OUTPUT_DIR, log_file):
    """
    Connects to AllerCatPro server, pastes the sequence in the textbox and downloads the resultant csv file. 
    
    Input:
    driver - initialised driver, with webdriver.enabled = False and useAutomationExtention = False.
    file = A file containing less than 50 protein sequences.    
    """

    print("Connecting to AllerCatPro...")
    driver.get('https://allercatpro.bii.a-star.edu.sg/')
    print("Connected")
    
    # collect all proteins in a single string (including the characters ">", "\n")
    with open(file_path, "r") as current_file:
        protein = ''.join(current_file.readlines())
    time.sleep(5)
    text_box = driver.find_element_by_xpath('//*[@id="seq"]')
    
    # send the protiens to the text box and wait for 2-5 seconds before pressing the submit button.
    text_box.send_keys(protein)
    print("FASTA Sequences for file {} sent.".format(file_name))
    
    submit_click_sleep = random.randint(2,5) 
    print("Sleeping for {}s before clicking submit.".format(submit_click_sleep))
    time.sleep(submit_click_sleep)
    
    #click the button
    for steps in range(2):
        try:
            driver.find_element_by_xpath('/html/body/center/font/form/input[2]').click()
        except:
            continue
        time.sleep(1)
    
    print("Running analysis")
    analysis_time = random.randint(60,65)
    print("Sleeping for {}s".format(analysis_time))
    time.sleep(analysis_time)
    
    try:
        URL = driver.find_element_by_xpath('/html/body/font/center/a').get_attribute('href')  #retrieve the URL of the temporary csv file generated
        print(URL)
        file_bin = requests.get(URL, verify=False) #shows error if we try to verify the SSL certificate - since it is a onetime throwaway script - i am skiping the verification.
        with open(OUTPUT_DIR+file_name+".csv", "wb") as out_f:
            out_f.write(file_bin.content)
        
        with open(OUTPUT_DIR+file_name+".csv", "r") as verify_f:
            Verify = (len(verify_f.readlines()) >= 49)
        if Verify:
            logging(log_file, "write", message="OK:{}".format(file_name))
        else:
            logging(log_file, "write", message="ERROR:{}".format(file_name))
        print("File Downloaded.")
    
    except:
        logging(log_file, "write", message="ERROR:{}".format(file_name))
        

########## checking the files and getting the file list ready ################

CURRENT_DIR = os.getcwd() #get the current working directory

try:
    PROTEIN_INPUT = str(input("\nEnter the name of the Protein file:")) # INPUT FILE
    file_name = str((PROTEIN_INPUT.split("\\")[-1]).split(".")[0]) #INPUT FILE NAME (WITHOUT EXTENTION)
    CUSTOM_FILE_START = str(input("Custom start? (Y/N):")) #if you want to start from a custom file
    CUSTOM_FILE_START_FLAG = "y" in CUSTOM_FILE_START.lower() #FLAG set to True if Y or y.
except FileNotFoundError:
    print("File not found.")
    sys.exit()

SPLIT_FILE_DIR_NAME = "Divided_files_" + file_name #FILES DIRECTORY
try:
    assert SPLIT_FILE_DIR_NAME in list(os.listdir(CURRENT_DIR))
except AssertionError:
    print("Split the file first and make sure your directory name is {}".format(SPLIT_FILE_DIR_NAME))
    sys.exit()    
    
with open(file_name+"_list.txt", "r") as list_file:
    SPLIT_FILE_LIST = list_file.readline().split(" ") #LIST OF FILES


if CUSTOM_FILE_START_FLAG:
    custom_file = str(input("Enter the exact name of the file:"))
    custom_file_name = '\\'.join(SPLIT_FILE_LIST[0].split("\\")[:-1]) + '\\'+custom_file + '.fasta'
    try:
        assert custom_file_name in SPLIT_FILE_LIST
    except AssertionError:
        print("{} is missing from Split file directory.".format(custom_file))
        sys.exit()

# make the output directory
OUTPUT_DIR = CURRENT_DIR + "\\OUTPUT_"+file_name+"\\"
try:
    os.mkdir(OUTPUT_DIR)
except FileExistsError:
    print("Output directory already exists.")


LOG_FILE_NAME = file_name+"_log.txt"
resume = False
    
if CUSTOM_FILE_START_FLAG == False: #if custom file flag is set to False took for log file.
    # check the log file first
    if LOG_FILE_NAME in os.listdir():
        file_last = logging(LOG_FILE_NAME, "read")
        resume = True
        if file_last == "-9":
            sys.exit()
        else:
            file_last_name = '\\'.join(SPLIT_FILE_LIST[0].split("\\")[:-1]) + '\\'+file_last + '.fasta'
            try:
                assert file_last_name in SPLIT_FILE_LIST
            except AssertionError:
                print("{} is missing from Split file directory.".format(file_last))
                sys.exit()


###############################################################################


# if not CUSTOM FILE FLAG and LOG FILE LAST is OK, resume the job
if resume == True:
    idx = SPLIT_FILE_LIST.index(file_last_name)
    SPLIT_FILE_LIST = SPLIT_FILE_LIST[idx+1 :]
    print("Resuming the operation after file {}".format(file_last))

#if CUSTOM FILE FLAG
if CUSTOM_FILE_START_FLAG:
    idx = SPLIT_FILE_LIST.index(custom_file_name)
    SPLIT_FILE_LIST = SPLIT_FILE_LIST[idx :]
    print("Resuming the operation from file {}".format(custom_file_name))
    

######################### Initializing the driver #############################

driver_path = r"C:\Users\Gurpi\gecko-firefox\geckodriver.exe"
PROFILE_PATH = "C:\\Users\\Gurpi\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\wnrjvym6.default-release"
print("Starting driver..")

profile = webdriver.FirefoxProfile(PROFILE_PATH)
profile.set_preference('dom.webdriver.enabled', False)
profile.set_preference('useAutomationExtention', False)
profile.update_preferences()
desired = DesiredCapabilities.FIREFOX


start = time.time()
driver = webdriver.Firefox(executable_path=driver_path, firefox_profile = profile, desired_capabilities=desired)
end1 = time.time()

print("Time taken to initialize driver {}s".format(round(end1-start, 2)))

###############################################################################

for path in SPLIT_FILE_LIST:
    path_name = (path.split("\\")[-1]).split(".")[0]
    AllerCatPro(driver, path, path_name, OUTPUT_DIR, LOG_FILE_NAME)
    end_sleep = random.randint(30,100)
    print("Sleeping for {}s".format(end_sleep))
    time.sleep(end_sleep)

        
##############################################################################

end2 = time.time()
print("Total time taken:", round(end2-start, 2), "s")
driver.close()








            
        