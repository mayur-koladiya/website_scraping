from bs4 import BeautifulSoup
import requests
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="automotive"
)



URL = 'https://www.automotivetouchup.com/touch-up-paint/volkswagen/2021/all-models/'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')


results = soup.find(id='ctl00_ctl00_OuterBodyContentPlaceHolder_OuterYearDropDownList')
job_elems = soup.find_all('table', class_='pears paint-codes')


years = []   
list = results.findAll('option')
for l in list:
    if l['value'] != "":
        
        year = l['value']
               
        url2 = 'https://www.automotivetouchup.com/touch-up-paint/volkswagen/'+year+'/all-models/'
        page2 = requests.get(url2)
        
        soup2 = BeautifulSoup(page2.content, 'html.parser')
        
        job_elems2 = soup2.find('h1', class_='fadeInUp animated').contents
        job_elems2 = job_elems2[0]        
        if job_elems2 != "NO MODELS":  
              
            number_of_rows = 0
            for row in soup2.find_all('table', class_='pears paint-codes'):
                number_of_rows = len(row.findAll('tr'))
            tr = 0   
                
            status = 0
            
            for x in range(1, number_of_rows):
                
              if status != 0:
                    break
              for row in soup2.find_all('table', class_='pears paint-codes'):
                second_column = row.findAll('tr')[x].contents
                
                try:
                    status = 0
                    first_column = second_column[1]
                    second = second_column[3]
                    third_column = second_column[5].contents
                    first_column = first_column.findAll('img')
                    
                    
                    mycursor = mydb.cursor()
                    
                    v1 = year
                    v2 = str(first_column[0].attrs.get('src'))
                    v3 = str(second.contents[0])
                    v4 = str(third_column[0])
                    
                    sql = "INSERT INTO volkswagen_python VALUES (%s,%s,%s,%s)"
                    mycursor.execute(sql,(v1,v2,v3,v4))
                    
                    mydb.commit()
                    print("data inserted...")
                    
                    #print (first_column[0].attrs.get('src'),second.contents[0],third_column[0]) 
                except:
                    status = 1
                    print("error")
