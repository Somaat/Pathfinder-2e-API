import re
from bs4 import BeautifulSoup

def trim_html(src, start, end):
    if start not in src or end not in src:
        return ''
    tmp = src[src.index(start)+len(start):src.index(end)]
    tmp = sanitize(tmp)
    return tmp

def ul_to_list(src):
    soup = BeautifulSoup(src, 'html.parser')
    items = []
    for li in soup.find_all("li"):
        items.append(li.string.strip())
    return items

def hxtitle(title, x):
    return f'<h{x} class="title">{title}</h{x}>'

def untitle(title):
    return re.sub('<h.*?>|</h.*?>', '', title)

def section_by_title(src, title):
    if title not in src:
        return ''

    tmp = src
    
    for x in ['2','3']:
        if hxtitle(title, x) in src:
            tmp = tmp[tmp.index(hxtitle(title,x))+len(hxtitle(title,x)):]
    
    if '<h' in tmp:
        tmp = tmp[:tmp.index('<h')]
    elif '</span>' in tmp:
        tmp = tmp[:tmp.index('</span>')]
    else:
        tmp = tmp[:tmp.index('<div')]
    tmp = sanitize(tmp)
    return tmp

def sanitize(src):
    tmp = src
    tmp = tmp.replace('<br/>','\n')
    tmp = tmp.replace('<i>','')
    tmp = tmp.replace('</i>','')
    tmp = tmp.replace(u'\u2014','--')
    tmp = tmp.replace(u'\u2019',"'")
    tmp = re.sub('<a.*?>|</a>', '', tmp)
    return tmp.strip()

def get_all(category):
        """ Returns a list of all h2 titles of the given type currently on AoN """
        scraped = []
        response = get(f'http://2e.aonprd.com/{category}.aspx')
        Ancestry.last_hit = datetime.datetime.now()
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = soup.find_all("h2", class_="title")
        if len(titles) == 0:
            return scraped
        links = [t.find_all("a")[-1] for t in titles]
        item_list = [[l.contents[0], 'http://2e.aonprd.com/' + l['href']] for l in links]
        for i in item_list:
            name = i[0]
            url = i[1]
            scraped.append([name, url])
        return scraped