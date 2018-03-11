def format_filename(s):
    """Take a string and return a valid filename constructed from the string.
Uses a whitelist approach: any characters not present in valid_chars are
removed. Also spaces are replaced with underscores.

Note: this method may produce invalid filenames such as ``, `.` or `..`
Prepend a date string like '2009_01_15_19_46_32_'
and append a file extension like '.txt', to avoid the potential of using
an invalid filename.
"""
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ', '_')  # replace spaces with underscores
    return filename

import pdfkit, requests, bs4, pprint
from PyPDF2 import PdfFileMerger, PdfFileReader

path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

finishing_root = 'https://www.finishing.com'
url_index = []
pagelinks = []
failedlinks =[]
ignorelinks = ['https://www.finishing.com/shops/index.html',
        'https://www.finishing.com/equipment/index.html',
        'https://www.finishing.com/chemicals/index.html',
        'https://www.finishing.com/consultants/index.html',
        'https://www.finishing.com/environmental/index.html',
        'https://www.finishing.com/testing/index.html',
        'https://www.finishing.com/home/about.html#contact',
        'https://www.finishing.com/home/privacy.html',
        'https://www.finishing.com/index.html',
        'https://www.finishing.com/letters/index.html',
        'https://www.finishing.com/search/searchgoogle.html']

for i in range(1):
    url_index.append(finishing_root + '/letters/archive' + str(i) + '000.html')
    res = requests.get(url_index[i])
    soup = bs4.BeautifulSoup(res.content)
    for link in soup.find_all('a', href = True):
        url = finishing_root + link['href'][2:]
        name = format_filename(link.get_text())
        if url not in ignorelinks:
            pagelinks.append(url)
            try:
                pdfkit.from_url(url,'C:\Finishing\\'+name+'.pdf',configuration=config)
            except:
                failedlinks.append(url)

print(failedlinks)
print('/n Trying to download failed-links again')

for url in failedlinks:
        pdfkit.from_url(url, 'C:\Finishing\\' + name + '1.pdf', configuration=config)
        failedlinks.remove(url)

print('The following links failed to download (2 attempts)/n')
print(failedlinks)

# path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
# config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
# for i, page in enumerate(pagelinks):
#     pdfkit.from_url(page, 'temp_'+str(i)+'.pdf',configuration=config)

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(pagelinks)
# print(len(pagelinks))