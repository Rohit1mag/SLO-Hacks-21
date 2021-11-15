import requests
import re 
from bs4 import BeautifulSoup
import pandas as pd


pd.set_option('display.max_columns', None)


def getTeacherLinks(link):
    
    #n_links={}
    pages=[]
    names=[]
    ratings=[]
    classes={}
    page=requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    full_container=soup.find_all("div", class_= re.compile("container full-width"))
    for instance in full_container:
        finds=instance.find_all("a", class_= re.compile("no-link-highlight text-muted filterable"))

        for find in finds:
            pages.append(find.get('href'))
    
        nameFinds=instance.find_all("strong", class_=re.compile("hidden-xs"))
        for name in nameFinds:
            names.append(name.text.strip().split("                           \n ")[0])
            #name=name.text
            # names.append(name.strip().split("                           \n")[0])
            ratings.append(name.text.strip().split("                           \n ")[1])
            ratings=[float(rating) if rating!='N/A' else 'N/A' for rating in ratings]
            
            # name=name.strip("                           </span>")
            # names.append(name.split('                           <span class="pull-right"><span class="glyphicon glyphicon-star star-color"></span>')[0])
    
    # print(names)

    pages=['https://polyratings.com'+page for page in pages]
    print("Here", pages, names, ratings)
    return pages, names, ratings


def scrape_classes(pages, names, ratings):
    full_classes={}
    index=0
    for page in pages[:300]:
        link=requests.get(page)
        soup = BeautifulSoup(link.content, 'html.parser')
        center_container=soup.find("center")
        div_container=center_container.find("div", class_=re.compile("row"))
        div_container2=div_container.find("div", class_=re.compile("col-xs-12 col-sm-8"))
        section_container=div_container2.find_all("section", class_=re.compile("group"))
        classes=[]
        for section in section_container:
            h2=section.find("h2")
            classes.append(h2.text)
        # print(classes)
        full_classes[names[index]]=classes
        index+=1

    return full_classes

def classDic(profDic):
    classes={}
    for key in profDic:
        for clas in profDic[key]:
            if clas not in classes.keys():
                classes[clas]=[key]
            
            else:
                classes[clas].append(key)

    return classes




    # index=0
    # pIndex=0
    # for page in pages:
    #     link=requests.get(page)
    #     soup = BeautifulSoup(link.content, 'html.parser')
    #     center_container=soup.find("center")
    #     div_container=center_container.find("div", class_=re.compile("row"))
    #     class_container=div_container.find_all("a", class_=re.compile("scrollAnimate"))
        # classes[names[index]].append(clas.text)
        # for clas in class_container:
        #     print(clas.text)
        # print(classes)
    #     classes[names[index]]=[]
    #     for clas in class_container:
    #         classes[names[index]].append(clas.text)
            
    #     # print(index, pIndex )
    #     index+=1
    #     pIndex+=1
    
    # print(classes)

        # for teacher in soup.find_all('a', class_= re.compile("no-link-highlight text-muted filterable")):
        # t_link=teacher.get('href')
        # n_links["someone"]=t_link
    
    #print(n_links)
    
pages, names, ratings=getTeacherLinks("https://polyratings.com/list.html")
# print(len(pages), len(names), len(ratings))
print(classDic(scrape_classes(pages, names, ratings)))






