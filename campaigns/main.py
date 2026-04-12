from lib import CampaignScraper, find_promises_page

cs = CampaignScraper()

davemccormick = cs.scrape_promises_single_page("https://www.davemccormickpa.com/day-one-promises/")
print("*****Dave McCormick's Promises******")
for i in davemccormick: print(i)
print("\n\n\n")
# angelaalsobrooks = scrape_promises_single_page("https://www.angelaalsobrooks.com/priorities")
# for i in angelaalsobrooks: print(i)
print("*****Jim Bank's Promises******")
jimbanks = cs.scrape_promises_single_page("https://banksforsenate.com/issues/")
for i in jimbanks: print(i)
print("\n\n\n")

print("****Jim Justice's Promises*****")
jimjusticepage = find_promises_page("https://jimjusticewv.com")
jimjustice = cs.scrape_promises_linked_pages(jimjusticepage)
for x in jimjustice: print(x)

def try_and_print_promises(url):
    senator = cs.scrape_promises_linked_pages(url)
    for x in senator: print(x)

print("****Lisa Blunt Rochester's Promises*****")
try_and_print_promises("https://lisabluntrochester.com/issues")
print("\n\n\n")
###
try_and_print_promises("https://www.angelaalsobrooks.com/priorities")

try_and_print_promises("https://banksforsenate.com/issues/")

try_and_print_promises("https://lisabluntrochester.com/issues/")

try_and_print_promises("https://www.johncurtis.org/issues/")

try_and_print_promises("https://gallegoforarizona.com/issues/")
################
try_and_print_promises("https://www.davemccormickpa.com/issues/")

try_and_print_promises("https://berniemoreno.com/")

try_and_print_promises("https://timformt.com/")

try_and_print_promises("https://elissaslotkin.org/priorities/")

try_and_print_promises("https://jimjusticewv.com/issues/")

try_and_print_promises("https://www.jonhustedforsenate.com/")

try_and_print_promises("https://ashleymoody.com/priorities/")

try_and_print_promises("https://www.adamschiff.com/plans/")

try_and_print_promises("https://www.andykim.com/issues/")

