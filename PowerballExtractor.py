from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from collections import Counter
import csv
import time
import sys
#function to get the data we need from the page we're on, iterates through the table and adds the date and numbers (minus the red ball as client requested) to a list and returns it.
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
#list to store all the different tables from each page
pages = []
#open selenium browser with fresh cookies so we can press the buttons needed to get to the table and click through the pages
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.delete_all_cookies()
driver.get("https://ohiolottery.com/WinningNumbers/CheckYourNumbers.aspx?page=1#3")
#accept cookies
cookiesButton = driver.find_element_by_name("p$lt$zoneFooter$CookieLawConsent$btnAllowAll")
cookiesButton.click()
#displays the table (starts on page 1)
displayResultsButton = driver.find_element_by_name("p$lt$zoneContent$pageplaceholder$p$lt$zoneContent$pageplaceholder$p$lt$tab_content_3$PowerballPastDraw$SubmitButton")
displayResultsButton.click()
#calls our getPagesResults function and add its results to the pages list. so this would be for page 1.
pages.append(getPagesResults())
#change to page 2
pageTwoButton = driver.find_element_by_id("p_lt_zoneContent_pageplaceholder_p_lt_zoneContent_pageplaceholder_p_lt_tab_content_3_PowerballPastDraw_olcPager_lvPager_ctrl1_hlPage")
pageTwoButton.click()
#calls our getPagesResults function and add its results to the pages list.
pages.append(getPagesResults())
#change to page 3
pageThreeButton = driver.find_element_by_id("p_lt_zoneContent_pageplaceholder_p_lt_zoneContent_pageplaceholder_p_lt_tab_content_3_PowerballPastDraw_olcPager_lvPager_ctrl2_hlPage")
pageThreeButton.click()
#calls our getPagesResults function and add its results to the pages list.
pages.append(getPagesResults())
#change to page 4
pageFourButton = driver.find_element_by_id("p_lt_zoneContent_pageplaceholder_p_lt_zoneContent_pageplaceholder_p_lt_tab_content_3_PowerballPastDraw_olcPager_lvPager_ctrl3_hlPage")
pageFourButton.click()
#calls our getPagesResults function and add its results to the pages list.
pages.append(getPagesResults())
#closes selenium browser
driver.quit()
#list for storing the sorted tables for writing to csv
final = []
#loop that counts how many times a number is shown on a page, sorts it by most common and adds to the final list.
for page in pages:
	pageTotals = []
	for row in page:
		pageTotals.extend(row[1])
	final.append(Counter(pageTotals).most_common())

print("Results sorted by time number appears descending. \n")
#loop that prints results from tables sorted by time number appears descending
for i, pageResult in enumerate(final, 1):
	print(f"Page: {i}")
	for numberpair in pageResult:
		print(f"""{numberpair[0]}: {numberpair[1]}""")

print("\n Results sorted by number ascending. \n")
#individual lists for each results in a list
linesToWrite = [[], [], [], []]
#loop that prints starting from 0 all the numbers on each page with how many times they appear, and adds to the linesToWrite list for writing to csv.
for i, pageResult in enumerate(final, 1):
	print(f"Page: {i}")
	pageResult.sort(key=lambda tup: tup[0])
	for numberpair in pageResult:
		print(f"""{numberpair[0]}: {numberpair[1]}""")
		linesToWrite[(i-1)].append(numberpair)
#writes all the lists with table results in linesToWrite, meaning you get 4 csv files, one for each page with the pages results.
for i in range(4):
	with open(f"Page{(i+1)}.csv", "w", newline="") as file:
		writer = csv.writer(file)
		writer.writerows(linesToWrite[i])
	file.close()
#gives time for the user to read all the numbers if they wish, and closes the script in 10 minutes
print("\n Operation complete, each page has been written as a seperate .csv file. Program will close in 10 minutes.")

time.sleep(600)
sys.exit()
