import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse

first_link = 'https://en.wikipedia.org/wiki/Special:Random'
dest_link = 'https://en.wikipedia.org/wiki/Philosophy'
article_chain = []
stack = []
listwithbracesdata = []
finalbracelist = []

def clearthelist(listwithbracesdata):
    for element in range(len(listwithbracesdata)):
        listwithbracesdata.pop(-1)    

def extractbraces(para):
    for letter in range(len(para)):
        if para[letter] == '(':
            [brace,number] = ['(',letter]
            stack.append([brace,number])
        elif para[letter] == ')':
            if len(stack) == 1 and stack[0][0] == '(':
                start = stack[-1][1]
                end = letter
                str2 = para[start+1:end]
                listwithbracesdata.append(str2)
                stack.pop(0)
                continue
            else:
                stack.pop(len(stack)-1)
    return listwithbracesdata

def filteras(bracecontent):
    if len(bracecontent) != 0:
        for element in range(len(bracecontent)):
            brace = BeautifulSoup(bracecontent[element],'html.parser')
            aass = brace.find_all("a")
            if len(aass)!=0:
                for everya in aass:
                    temp = everya.get('href')
                    finalbracelist.append(temp)    
    return finalbracelist
        
        

def is_absolute(url):
    return bool(urlparse(url).netloc)

def find_first_link(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html,'html.parser')
    content_div = soup.find_all("p",limit=3)
    for para in content_div:
        temp = str(para)
        bracecontent = extractbraces(temp)
        listinsidebraces = filteras(bracecontent)
#        print(listinsidebraces)
        clearthelist(listwithbracesdata)
        for element in para.find_all("a",recursive=False):
            if len(element)<1:
                continue
            else:
                res=element.get('href')
                if is_absolute(res):
                    continue
                elif res not in listinsidebraces:
                    clearthelist(listinsidebraces)
                    return 'https://en.wikipedia.org' + res
                    break
                else:
                    continue
    
def continue_crawl(search_history, target_url, max_steps=25):
    if search_history[-1] == target_url:
        print("We've found the target article!")
        return False
    elif len(search_history) > max_steps:
        print("The search has gone on suspiciously long, aborting search!")
        return False
    elif search_history[-1] in search_history[:-1]:
        print(search_history[-1])
        print("We've arrived at an article we've already seen, aborting search!")
        return False
    else:
        return True

article_chain.append(find_first_link(first_link))
while continue_crawl(article_chain,dest_link):
    recent = article_chain[-1]
    print(recent)
    result = find_first_link(recent)
    article_chain.append(result)
    time.sleep(2)

##result = find_first_link(first_link)
##print(result)
