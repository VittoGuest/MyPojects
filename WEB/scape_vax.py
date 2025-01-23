import bs4
import requests
import pprint
import datetime
import locale
import webbrowser

pdf_source = 'https://sansol.isan.csi.it/api/apisanvac/api/v1/cittadini/FNTVTR93T16E020Y/documenti/'
main_page= 'https://sansol.isan.csi.it/la-mia-salute/vaccinazioni/#/home/vaccini-effettuati'
#res = requests.get(url=main_page)
#res.raise_for_status()

'''file = open('C:\\Users\Berdyna Tech\\Documents\\My New Projects\\WEB\\Vaccinazioni _ Salute Piemonte.html', 'r')
page = bs4.BeautifulSoup(file.read(), 'html.parser')

divs = page.find_all('div','q-item__section column q-item__section--main justify-center')

date_raw = []
for i in divs:
    text = i.select('div div')
    for x in text:
        date_raw.append(x.getText())

data = []
for i in date_raw:
    result = i.split('\n')
    if 'Effettuato' in result[1]:
        data.append(result[2].strip())

print(data)
file.close()'''
locale.setlocale(locale.LC_TIME, 'it_IT')
month = {'Mag':'05', 'Mar':'03','Gen':'01', 'Giu':'06', 'Dic': '12', 'Ott':'10', 'Feb':'02', 'Nov':'11'}

data = ['29 Mag 2021', '20 Mar 2021', '12 Gen 2010', '12 Gen 2010', '12 Gen 2010', '15 Giu 2005', 
        '15 Giu 2005', '15 Giu 2005', '09 Dic 1999', '09 Dic 1999', '09 Dic 1999', '09 Ott 1997', 
        '09 Ott 1997', '09 Ott 1997', '22 Feb 1996', '11 Nov 1994', '11 Nov 1994', '11 Nov 1994', 
        '11 Nov 1994', '11 Nov 1994', '09 Mag 1994', '09 Mag 1994', '09 Mag 1994', '09 Mag 1994', 
        '09 Mag 1994', '18 Mar 1994', '18 Mar 1994', '18 Mar 1994', '18 Mar 1994', '18 Mar 1994']

for i in data:
    date_object = datetime.datetime.strptime(i, '%d %b %Y')

    # Format the datetime object to the desired format
    formatted_date = date_object.strftime('%Y-%m-%d')+'T00:00:00/pdf'
    result = pdf_source+formatted_date
    webbrowser.open(result)
    