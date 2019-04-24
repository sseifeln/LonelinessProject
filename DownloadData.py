import requests #pip install requests if you don't already have this  
from lxml import html # also with lxml if this is not available 

# because this is easier .. and was curious to see if you can do this 
def downloadFile(url,fileName):
    r = requests.get(url, stream = True) 
    with open(fileName,"wb") as fileToWrite: 
        for chunk in r.iter_content(chunk_size=1024): 
             # writing one chunk at a time to file 
             if chunk: 
                 fileToWrite.write(chunk) 

# lets see if I can figure out whats available to download from the html on the page 
# apparently yes... see : https://docs.python-guide.org/scenarios/scrape/
def decodePage(url):
    r = requests.get(url)
    tree = html.fromstring(r.content)
    xmlStr = '//a[@data-ga-event=\"download\"]/text()'
    #This will create a list of files available to download 
    tagInfo = tree.xpath(xmlStr)
    #will this get the list of urls?
    #print(tagInfo)
    #https://lxml.de/3.1/api/private/lxml.html.HtmlElement-class.html
    xmlStr = '//table//tr//td//a'#tr[@class=\" dgu-datafile\"]/text()'
    tagInfo = tree.xpath(xmlStr)
    fileIndex=0
    for tag in tagInfo : 
        publisher = tag.get('publisher')
        label = tag.get('aria-label')
        refUrl = tag.get('href')
        if( '.zip' in refUrl or '.csv' in refUrl):
            # figure out a smarter way to label these..
            print(label, ' - ', refUrl)
            refUrl_split=refUrl.split('.')
            fileName='f%d.%s'%(fileIndex,refUrl_split[len(refUrl_split)-1])
            downloadFile(refUrl,fileName)
            fileIndex+=1
    return tagInfo




