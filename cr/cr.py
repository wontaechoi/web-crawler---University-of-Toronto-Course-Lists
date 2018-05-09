import requests
import time
from bs4 import BeautifulSoup

def get_courses():
    url = 'https://fas.calendar.utoronto.ca/search-courses'
    code = requests.get(url)
    text = code.text
    soup = BeautifulSoup(text, 'html.parser')

    link =soup.find(attrs={"class" :"pager-current"})
    current_page = int(link.get_text().split('of')[0])
    total_page = int(link.get_text().split('of')[1])
    course_list = []

    link = soup.find(attrs={"class": "views-table cols-5"})
    link1 = link.find('tbody')
    for link2 in link1.find_all(attrs={"class": "views-field views-field-title"}):
        course_list.append(link2.get_text().strip())

    while  (current_page < total_page):
        url = 'https://fas.calendar.utoronto.ca/search-courses?page=' + str(current_page)
        code = requests.get(url)
        text = code.text
        soup = BeautifulSoup(text, 'html.parser')
        link = soup.find(attrs={"class": "views-table cols-5"})
        if link is None:
            link = soup.find(attrs={"class": "views-table cols-4"})
        link1 = link.find('tbody')
        for link2 in link1.find_all(attrs={"class": "views-field views-field-title"}):
            course_list.append(link2.get_text().strip())

        current_page += 1
    return course_list

if __name__ == '__main__':

    course_list = get_courses()
    f = open('courselist.txt', 'w', encoding='utf-8')
    for course in course_list:
        f.write(course[:6]+ ', ' + course[6] + '\n')
    f.close()


