import unicodecsv as csv
from os import path
import requests
from BeautifulSoup import BeautifulSoup

# define where results will be stored
result = path.relpath('/home/all_auctions.csv')


# function for replacing some text later on
def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

auctions = {145, 142, 141, 143, 149, 151, 152, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 171, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194}	
	
alttxt = {'&#39;':' ', '&euro;':'', '&bull;':'', '&#232;':'e', '&#235':'e', '&#233;':'e', '&#224;':'a', '&amp;':'et', '&#244;':'o', '&#241;':'n', '&omicron;':'', ';':'', '&#226':'a'}

maanden = {'januari':'1', 'februari':'2', 'maart':'3', 'april':'4', 'mei':'5', 'juni':'6', 'juli':'7', 'augustus':'8', 'september':'9', 'oktober':'10', 'november':'11', 'december':'12'}

# define auctions (check http://www.veilingsylvies.be/nl/afgelopen-veilingen)
for auction in auctions: 
	
    # request first page of auction
    url = 'http://www.veilingsylvies.be/nl/veiling/%d' % auction
    response = requests.get(url)
    response.encoding = 'utf-8'
    html = response.content
    soup = BeautifulSoup(html.decode('utf-8','ignore'))
	
    # get month and year
	#soup = BeautifulSoup(html)
    titel = soup.find('title')
    titeltxt = titel.text
    splitted = titeltxt.split()
    maand = replace_all(splitted[6], maanden)
    jaar = splitted[7]

    # get auction lots
    table = soup.find('ul', attrs={'class': 'auction_lots'})

    list_of_rows = []
    for row in table.findAll('li')[1:]:
        list_of_cells = []
        list_of_cells.append(auction)
        list_of_cells.append(jaar)
        list_of_cells.append(maand)
        for cell in row.findAll('p'):
            text = replace_all(cell.text, alttxt)
            list_of_cells.append(text)
        if len(list_of_cells) <= 11:
	        list_of_rows.append(list_of_cells)

    outfile = open(result, "a")
    writer = csv.writer(outfile, delimiter =';', dialect='excel', encoding='utf-8')
    writer.writerow(["auction_nr", "jaar", "maand", "lot_nr", "lot_name", "lot_description", "lot_bottle", "lot_bottle_type", "lot_estimate", "lot_my_bid", "Resultaat"])
    writer.writerows(list_of_rows)

    # determine number of iterations
    tabel = soup.find('div', attrs={'class': 'pager'})
    lijst = []
    for rij in tabel.findAll('a')[1:]:
        lijst.append(rij.text)
    l = int(lijst[4])+1  
	
    # request next pages with auction results	
    for i in range(2, l): 	
        url = "http://www.veilingsylvies.be/nl/veiling/%d?sort=lotnr_asc&page=%d" % (auction, i)
        response = requests.get(url)
        response.encoding = 'utf-8'
        html = response.content
        soup = BeautifulSoup(html.decode('utf-8','ignore'))  
        table = soup.find('ul', attrs={'class': 'auction_lots'})

        list_of_rows = []
        for row in table.findAll('li')[1:]:
            list_of_cells = []
            list_of_cells.append(auction)
            list_of_cells.append(jaar)
            list_of_cells.append(maand)
            for cell in row.findAll('p'):
                text = replace_all(cell.text, alttxt)
                list_of_cells.append(text)
            if len(list_of_cells) <= 11:
	            list_of_rows.append(list_of_cells)

        outfile = open(result, "a")
        writer = csv.writer(outfile, delimiter =';', dialect='excel', encoding='utf-8')
        writer.writerows(list_of_rows)
