from bs4 import BeautifulSoup
import os
import requests
#import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import glob
from fpdf import FPDF
from PyPDF2 import PdfFileMerger
 
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--headless')
options.add_argument("--test-type")

driver = webdriver.Chrome(chrome_options=options)
 
#try and get it to use input()
x = "http://scribd.com/login"
driver.get(x)
time.sleep(5)
print("enter login_or_email")
user = input()
print("Enter password")
password = input()

driver.find_element_by_css_selector("#login_or_email").send_keys(user)
driver.find_element_by_css_selector("#login_password").send_keys(password)

driver.find_element_by_css_selector(".submit_btn").click()

#enter the url
print("\n\nEnter the url of the book")
url = input()
#url = 'https://www.scribd.com/read/254663574/The-Alchemist'
driver.get(url)

#wait for page to load
time.sleep(10)

#fullscreen css
page = driver.page_source
soup = BeautifulSoup(page, 'html.parser')
page_Count = soup.find('div',{'class':'page_counter'}).getText()
#has the number of pages in the books
pageNum = int(page_Count.split()[-1])

for x in range(pageNum):
	time.sleep(2)
	driver.save_screenshot(str(x) + ".png")
	driver.find_element_by_css_selector(".page_right").click()



driver.close()

#now we gather all the pngs and turn into pdf
split_url  = url.split("/")
book_name = split_url[-1] 
pdffolder = glob.glob('*.png')
#creates list of files that end in .png
file_lst = []
lastFileNumber = 0

#puts the files in order
for num in range(len(pdffolder)):
	file_lst.append(glob.glob(str(num) + '.png'))

#file_lst will have the location for all the pdf files to be merged

#this is where the merged pdf will go
output_path =  "book_name.pdf"
pdf = FPDF('P', 'in') 

for file in file_lst:
	pdf.add_page()
	pdf.image(file[0],w=pdf.w, h=pdf.h/1.5)
pdf.output(output_path)


#clean up the pngs
for file in file_lst:
	os.remove(file[0])
