import requests #pip install requests if you don't already have this  
from lxml import html # also with lxml if this is not available 
import os
from tqdm import tqdm #I want a progress bar...
import requests
import xlrd
import csv

 

# from TDQM docs https://github.com/tqdm/tqdm#hooks-and-callbacks

# this one seems to work the best 
# https://gist.github.com/wy193777/0e2a4932e81afc6aa4c8f7a2984f34e2
def download_from_url(url, dst, chunk_size=1024*2):
    file_size = int(requests.head(url).headers["Content-Length"])
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    pbar = tqdm( total=file_size, initial=first_byte, unit='B', unit_scale=True, desc=url.split('/')[-1])
    req = requests.get(url, headers=header, stream=True)
    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size):
            if chunk:
                f.write(chunk)
                pbar.update(chunk_size)
    pbar.close()
    return file_size

# lets see if I can figure out whats available to download from the html on the page 
# apparently yes... see : https://docs.python-guide.org/scenarios/scrape/
def decodePage(url):
    #make data dir
    os.system('mkdir -p data')
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
        if( '.zip' in refUrl or '.csv' in refUrl and label != None ):
            # figure out a smarter way to label these..
            refUrl_split=refUrl.split('.')
            print(label, ' - ', refUrl) 
            labels=(label.split('dataset:'))
            description=labels[len(labels)-1].split('-')[0].strip().replace(' ', '_')
            print(description)
            fileName='data/f%d.%s'%(fileIndex,refUrl_split[len(refUrl_split)-1])
            if( fileIndex == 0): 
                download_from_url(refUrl, fileName,1024*32)
            fileIndex+=1
    return tagInfo


def csv_from_excel():

    wb = xlrd.open_workbook('your_workbook.xls')
    sh = wb.sheet_by_name('Sheet1')
    your_csv_file = open('your_csv_file.csv', 'wb')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in xrange(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()


