from selenium import webdriver
from selenium.webdriver.common.by import By
import time, urllib, requests, os, urllib.request

# Pre script, we need to navigate to the folder we want all information to be within.
os.chdir(r"C:\Users\cvela\MyPythonScripts\FakeCarDealership")


#                           Step 1: LOG IN
#opens browser and goes to website
browser = webdriver.Firefox()
browser.get('https://anonymouscarwebsite.com')

#fills our login portion username
loginElem = browser.find_element(By.CSS_SELECTOR, '#accountName')
loginElem.send_keys('FakeUserID')

#fills out login portion password
loginElemPass = browser.find_element(By.CSS_SELECTOR, '#password')
loginElemPass.send_keys('FakePassword')

#submit the pass and username
loginElem.submit()


#gives next page time to load, will crash without (possibly could have a shorter pause)
time.sleep(7)

#                           Step 2: Go To Purchased Cars
# click drop down,  will crash without
pageElem = browser.find_element(By.CSS_SELECTOR, 'div.user-config')
pageElem.click()

# click purchase page 
purElem = browser.find_element(By.CSS_SELECTOR, 'div.user-config > div:nth-child(3) > a:nth-child(5)')
purElem.click()

#gives next page time to load, will crash without
time.sleep(5)

#                           Step 3: Download Purchased Cars
# All other portions of the script lead to this moment
# There's alot of code BECAUSE this is the main work force of my code.
#
#
# sets cars to 'purchased within last 18 months'
timeElem = browser.find_element(By.CSS_SELECTOR, '#recent_last18Months')
timeElem.click()

#gives time for cars to load
time.sleep(5)


# builds hyperlinks of cars by using the fact that these cars all start
# with the year in their name 
carList = []
carElem = browser.find_elements(By.CSS_SELECTOR, 'a')
for car in carElem:
	if car.text[:2] == '20' or car.text[:2] == '19':
		carList.append(car)
		
#click on every car link, get data
for i in range(len(carList)):
        carList[i].click()
        time.sleep(5)

        #Portion for getting car info, I want the VIN, the odometer,  YMM and pictures
        #gets vin
        vinElem = browser.find_element(By.CSS_SELECTOR, '#vdp_mps_vin')
        vin = vinElem.text

        #gets odometer 
        odoElem =  browser.find_element(By.CSS_SELECTOR, '#mps_vdp_mileage')
        odo = odoElem.text

        #gets year, make, model. Simplified to YMM
        YMMElem = browser.find_element(By.CSS_SELECTOR, '#vehicle_info_title_ymm')
        YMM = YMMElem.text


        # gets pics in a url format, currently in thumbnails
        picMap = {}
        for index in range(5):
                picElems = browser.find_elements(By.CSS_SELECTOR, 'img')
                for pic in picElems:
                        if 'https://adesa.kar' in pic.get_attribute('src') and pic.get_attribute('src')[-7:] == "_th.jpg":
                                if pic not in picMap:
                                        picMap[pic.get_attribute('src')] = 1
                                else:
                                        continue
                browser.find_element(By.CSS_SELECTOR, '#next').click()
                time.sleep(3)
                
        #Goes through picmap and converts those thumbnail pics into full length images
        for pic in picMap.copy():
            newurl = pic[:-7] + '.jpg'
            del picMap[pic]
            picMap[newurl] = 1

        # visual inspection to show what car we're currently working on.
        print(YMM, odo, vin)
        # create a directory named as YMM + vin
        # AS OF RIGHT NOW SCRIPT FAILS IF OLD FILE EXISTS
        # I need to think of a work around for this, either I delete the old files
        # I move them somewhere? I overwrite? my original Idea was to delete these files when I uploaded them.
        # This is a simple design info I just need to make a decision on at a later date
        os.mkdir('C:\\Users\\cvela\\MyPythonScripts\\FakeCarDealership' + '\\' + YMM + ' ' + vin)

        #go to the directory created
        os.chdir('C:\\Users\\cvela\\MyPythonScripts\\FakeCarDealership' + '\\' + YMM + ' ' + vin)

        
        # open a file, name it carInfo.txt, write YMM, odo, vin info
        carInfoText = open("carInfo.txt", "w")
        carInfoText.write(YMM + '|' + odo + '|' + vin)
        carInfoText.close()
        


        # using the picMap which is currently populated with URL format of pics
        # we then turn that URL into a .png and download it
        i = 0
        for url in picMap:
            print(url)
            urllib.request.urlretrieve(url, "screenshot" + str(i) + ".png")
            i += 1
        

        #go back to the main directory so that on next iteration the car file will be created in main
        os.chdir(r"C:\Users\cvela\MyPythonScripts\FakeCarDealership")
        #changes browser to the main buying page
        browser.back()
        time.sleep(5)
        # recreate the carList, for some reason, it will break without this.
        # not sure why. will see if I can fix this later?
        timeElem = browser.find_element(By.CSS_SELECTOR, '#recent_last18Months')
        timeElem.click()
        time.sleep(5)
        carList = []
        carElem = browser.find_elements(By.CSS_SELECTOR, 'a')
        for car in carElem:
                if car.text[:2] == '20' or car.text[:2] == '19':
                        carList.append(car)
browser.quit()






