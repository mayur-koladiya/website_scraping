from selenium import webdriver 
import time 
from bs4 import BeautifulSoup
import requests
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="village_data"
)



driver = webdriver.Chrome()  
driver.get("https://www.pmkisan.gov.in/Rpt_BeneficiaryStatus_pub.aspx")

village = "Khajuri-Pipaliya  -  (515405)"

#print(driver.page_source)  

driver.find_element_by_xpath("//select[@name='ctl00$ContentPlaceHolder1$DropDownState']/option[text()='GUJARAT']").click()
time.sleep(6)
driver.find_element_by_xpath("//select[@name='ctl00$ContentPlaceHolder1$DropDownDistrict']/option[text()='AMRELI']").click()
time.sleep(5)
driver.find_element_by_xpath("//select[@name='ctl00$ContentPlaceHolder1$DropDownSubDistrict']/option[text()='Kunkavav Vadia']").click()
time.sleep(5)
driver.find_element_by_xpath("//select[@name='ctl00$ContentPlaceHolder1$DropDownBlock']/option[text()='KUNKAVAV -VADIA']").click()
time.sleep(6)
driver.find_element_by_xpath("//select[@name='ctl00$ContentPlaceHolder1$DropDownVillage']/option[text()='"+village+"']").click()
time.sleep(6)

driver.find_element_by_id('ContentPlaceHolder1_btnsubmit').click()







time.sleep(10)

#print(driver.page_source)

code = driver.page_source
soup = BeautifulSoup(code, 'html.parser')
job_elems = soup.find_all('table', class_='table table-striped table-bordered table-list')
soup = job_elems[0]

#print(job_elems[0])



#driver.find_element_by_css_selector('#ContentPlaceHolder1_GridView1 > tbody > tr:nth-child(53) > td > table > tbody > tr > td:nth-child(2) > a').click()


"""

with open("ipython.html", "r") as f:    
    contents = f.read()
"""
    
#soup = BeautifulSoup(job_elems[0], 'html.parser')






#print(number_of_rows)


number_of_rows = len(soup.findAll('tr')) - 4

#row = soup.find_all('table', class_='table table-striped table-bordered table-list')

#ele = row.findAll('tr')[10].contents
page_total = soup.findAll('tr')[number_of_rows+2].contents
page_total = page_total[1].findAll('tbody')
total = len(page_total[0].findAll('td'))

#print(total)


for x1 in range(1, total+1):
    
    #print("page : " , x1)


    
   
    code = driver.page_source
    soup = BeautifulSoup(code, 'html.parser')
    job_elems = soup.find_all('table', class_='table table-striped table-bordered table-list')
    soup = job_elems[0]
    
    number_of_rows = len(soup.findAll('tr')) - 4
    
    for x in range(1, number_of_rows+1):
        second_column = soup.findAll('tr')[x].contents
    
        mycursor = mydb.cursor()
        #print(second_column[2].span.text)
        
        v1 = second_column[2].span.text
        
        sql = "INSERT INTO farmer_name VALUES (%s,%s)"
        
        mycursor.execute(sql,(v1,village))
        
        mydb.commit()
        print(v1,"   inserted")
        #print(x)
    
    
    
    #print(len(second_column[0].findAll('td')))
    #page_total = page_total[0].findAll('td')
    
    #print(second_column[1])
        
    time.sleep(10)
    
 

    #a = str1.replace('"', "'") 
    if x1 != total:
        str1 = str(x1+1)
        try :
            driver.find_element_by_link_text(str1).click()
        except :
            element = driver.find_element_by_link_text(str1)
            driver.execute_script("arguments[0].click();", element)
            
    #driver.find_element_by_xpath(u'//a[text()="3"]').click()
    #link = driver.find_element_by_link_text(str1)
    #link.click()
    time.sleep(6)
    #driver.find_element_by_css_selector('#ContentPlaceHolder1_GridView1 > tbody > tr:nth-child(53) > td > table > tbody > tr > td:nth-child(2) > a').click()
     
    