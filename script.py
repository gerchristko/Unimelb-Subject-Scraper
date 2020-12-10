import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import csv
from lxml import etree

# function for data collecting
def subject_analysis(subjects, index):

    subject = subjects.pop(0)
    page = requests.get(subject)
    soup_in = BeautifulSoup(page.text, 'html.parser')

    title = soup_in.find('span', class_ = 'header--course-and-subject__main').text
    pattern = '([\w]{4}[\d]{5})'
    head = re.findall(pattern, title)
    course = title[:-12]
    code = head[0]
    fac, field = faculty(code)
    
    availability = soup_in.find_all("tr")[1].td
    divs = availability.find_all('div')
    
    sems = []
    sems_reg = []
    pattern = 'Semester \d|Summer|Winter'
    for i in range(len(divs)):
        offer = divs[i].text
        sems.append(offer)
        head = re.findall(pattern, offer)
        sems_reg.append(head)
    sem1 = "Not Offered"
    sem2 = "Not Offered"
    summer = "Not Offered"
    winter = "Not Offered"
    if (["Semester 1"] in sems_reg):
        sem1 = "Offered"
    if (["Semester 2"] in sems_reg):
        sem2 = "Offered"
    if (["Summer"] in sems_reg):
        summer = "Offered"
    if (["Winter"] in sems_reg):
        winter = "Offered"
        
    print(str(index+1) +". "+course," - ", code)      
    df.loc[index] = [course, code, field, fac, sem1, sem2, summer, winter]
# function for data collecting


# function to retrieve subjects
def collect_subjects(subjects):
    
    layer = soup.find_all('a', class_ = 'search-result-item__anchor')
    for i in range(len(layer)):
        href = layer[i]['href']
        next_url = base_url + href
        subjects.append(next_url)
# function to retrieve subjects
    
    
# function to retrieve faculty
def faculty(code):
    
    status = False
    code = code[:-5]
    xmltree = etree.parse("faculties.xml")
    root = xmltree.getroot()
    for faculties in root:
       for fields in faculties:
           #print(fields.get('name')," - ", fields.get('code'))
           if code == fields.get('code'):
               fac = faculties.get('name')
               field = fields.get('name')
               status = True
               break
       if (status):
           break
    try:
        return fac, field
    except:
        return 'Others', 'Others'
# function to retrieve faculty

# open csv file
FILENAME = 'Subjects.csv'
file = open(FILENAME ,'w+')
writer = csv.writer(file)
# open csv file


# open xml file
f = open("faculties.xml", "r")
text = f.read()
# open xml file


# create dataframe
df = pd.DataFrame(columns = ['Subject', 'Code', 'Area of study', 'Faculty', 
                             'Semester 1', 'Semester 2', 'Summer term', 'Winter term'])
# create dataframe


# url set up
base_url = 'https://handbook.unimelb.edu.au/'
url = 'https://handbook.unimelb.edu.au/search?types%5B%5D=subject&year=2021&subject_level_type%5B%5D=undergraduate&subject_level_type%5B%5D=Honours&study_periods%5B%5D=semester_1%7Csemester_1_%28early-start%29%7Csemester_1_%28extended%29&study_periods%5B%5D=semester_2%7Csemester_2_%28early-start%29%7Csemester_2_%28extended%29&study_periods%5B%5D=summer_term&study_periods%5B%5D=winter_term&area_of_study%5B%5D=all&org_unit%5B%5D=all&campus_and_attendance_mode%5B%5D=all&page=1&sort=_score%7Cdesc'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
# url set up


# scraping page 1
index = 0
pages = []
subjects = []
collect_subjects(subjects)

while(subjects):
        subject_analysis(subjects, index)
        index += 1

next_page = soup.find('a', rel = 'next')['href']
next_url = base_url + next_page
pages.append(next_url)
# scraping page 1


# web scraping
while(pages):
    # parse current page
    url = pages.pop(0)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    # parse current page
    
    # retrieve next page
    try:
        next_page = soup.find('a', rel = 'next')['href']
        next_url = base_url + next_page
        pages.append(next_url)
    except TypeError:
        k = 0
    # retrieve next page
    
    # retrieve subjects in current page
    collect_subjects(subjects)
    # retrieve subjects in current page
    
    # collect data in subjects page
    while(subjects):
        subject_analysis(subjects, index)
        index += 1
    # collect data in subjects page
    
# web scraping


# copy data to csv file
df.index += 1
df.to_csv(r'Subjects.csv')
# copy data to csv file


file.close()
f.close()
