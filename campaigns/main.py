from lib import scrape_promises_single_page

#
davemccormick = scrape_promises_single_page("https://www.davemccormickpa.com/day-one-promises/")
print("*****Dave McCormick's Promises******")
for i in davemccormick: print(i)
print("\n\n\n")
# angelaalsobrooks = scrape_promises_single_page("https://www.angelaalsobrooks.com/priorities")
# for i in angelaalsobrooks: print(i)
print("*****Jim Bank's Promises******")
jimbanks = scrape_promises_single_page("https://banksforsenate.com/issues/")
for i in jimbanks: print(i)
print("\n\n\n")