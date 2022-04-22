from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from collections import Counter
import csv
import time
import sys

def getPagesResults():
	rows = []
	table = driver.find_element_by_class_name("past_winning_numbers_results")
	for row in table.find_elements_by_css_selector("tr"):
		rowCells = []
		for cell in row.find_elements_by_tag_name("td"):
			if cell.get_attribute("class") == "pastDraws_date cyn_date":
				rowCells.append(cell.text)
			if cell.get_attribute("class") == "pastDraws_numbers cyn_numbers":
				for wrapper in cell.find_elements_by_class_name("cyn_numbers_wrap"):
					rowCells.append([int(number.get_attribute("value")) for number in wrapper.find_elements_by_class_name("number_input")][:-1])
		rows.append(rowCells)
	rows.pop(0)
	return(rows)

pages = []

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.delete_all_cookies()
driver.get("https://ohiolottery.com/WinningNumbers/CheckYourNumbers.aspx?page=1#3")

cookiesButton = driver.find_element_by_name("p$lt$zoneFooter$CookieLawConsent$btnAllowAll")
cookiesButton.click()

displayResultsButton = driver.find_element_by_name("p$lt$zoneContent$pageplaceholder$p$lt$zoneContent$pageplaceholder$p$lt$tab_content_3$PowerballPastDraw$SubmitButton")
displayResultsButton.click()

pages.append(getPagesResults())

pageTwoButton = driver.find_element_by_id("p_lt_zoneContent_pageplaceholder_p_lt_zoneContent_pageplaceholder_p_lt_tab_content_3_PowerballPastDraw_olcPager_lvPager_ctrl1_hlPage")
pageTwoButton.click()

pages.append(getPagesResults())

pageThreeButton = driver.find_element_by_id("p_lt_zoneContent_pageplaceholder_p_lt_zoneContent_pageplaceholder_p_lt_tab_content_3_PowerballPastDraw_olcPager_lvPager_ctrl2_hlPage")
pageThreeButton.click()

pages.append(getPagesResults())

pageFourButton = driver.find_element_by_id("p_lt_zoneContent_pageplaceholder_p_lt_zoneContent_pageplaceholder_p_lt_tab_content_3_PowerballPastDraw_olcPager_lvPager_ctrl3_hlPage")
pageFourButton.click()

pages.append(getPagesResults())

driver.quit()

final = []

for page in pages:
	pageTotals = []
	for row in page:
		pageTotals.extend(row[1])
	final.append(Counter(pageTotals).most_common())

print("Results sorted by time number appears descending. \n")

for i, pageResult in enumerate(final, 1):
	print(f"Page: {i}")
	for numberpair in pageResult:
		print(f"""{numberpair[0]}: {numberpair[1]}""")

print("\n Results sorted by number ascending. \n")

linesToWrite = [[], [], [], []]

for i, pageResult in enumerate(final, 1):
	print(f"Page: {i}")
	pageResult.sort(key=lambda tup: tup[0])
	for numberpair in pageResult:
		print(f"""{numberpair[0]}: {numberpair[1]}""")
		linesToWrite[(i-1)].append(numberpair)

for i in range(4):
	with open(f"Page{(i+1)}.csv", "w", newline="") as file:
		writer = csv.writer(file)
		writer.writerows(linesToWrite[i])
	file.close()

print("\n Operation complete, each page has been written as a seperate .csv file. Program will close in 10 minutes.")

time.sleep(600)
sys.exit()