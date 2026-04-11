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