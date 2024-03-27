import time
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from tkinter import messagebox
from tkinter import ttk


# Function to open Chrome incognito window
def open_chrome_incognito():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


# Function to search for a given string in Google
def search_google(driver, query):
    driver.get("https://www.google.es")
    # Accept cookies
    try:
        WebDriverWait(driver, 9).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Aceptar todo']"))).click()
    except:
        pass  # If the accept button is not found or already accepted, continue

    # Wait for the search box to be clickable
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "gLFyf"))
    )

    # Find the search box and submit the query
    search_box = driver.find_element(By.CLASS_NAME, "gLFyf")
    search_box.send_keys(query)
    search_box.submit()
    time.sleep(2)  # Wait for the results to load
    return driver


# Function to extract search results from Google
def extract_results(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('h3', class_="LC20lb MBeuO DKV0Md")[:10]  # Extracting first 10 results
    return [result.text for result in results]


# Function to handle search button click
def search_button_click():
    query1 = entry1.get()
    query2 = entry2.get()
    query3 = entry3.get()
    query4 = entry4.get()
    query5 = entry5.get()

    # Combine queries into a list
    queries = [query1, query2, query3, query4, query5]

    # Open incognito tabs only for non-empty queries
    drivers = []
    for query in queries:
        if query:  # Check if the query is not empty
            drivers.append(open_chrome_incognito())
        else:
            drivers.append(None)  # Placeholder for empty query

    # Search for each non-empty query in each tab
    for i, (driver, query) in enumerate(zip(drivers, queries), start=1):
        if driver:  # Check if the driver exists (for non-empty queries)
            try:
                driver.execute_script("window.open('about:blank', '_blank');")
                driver.switch_to.window(driver.window_handles[-1])
                driver = search_google(driver, query)
            except Exception as e:
                print(f"Error occurred while processing tab {i}: {e}")

    # Extract and display results from each tab
    results = []
    for driver in drivers:
        if driver:  # Check if the driver exists (for non-empty queries)
            try:
                results.append(extract_results(driver))
            except Exception as e:
                print(f"Error occurred while extracting results: {e}")
                results.append([])  # Append empty list for failed queries

    # Display results in a table
    max_results = max(len(result) for result in results)  # Get the maximum number of results
    for i in range(max_results):
        values = [results[j][i] if j < len(results) and i < len(results[j]) else "" for j in range(5)]
        treeview.insert('', 'end', values=values)


# Creating UI
root = tk.Tk()
root.iconbitmap("icon.ico")
root.title("Keyword Lister")

frame = tk.Frame(root)
frame.pack(pady=10)

label1 = tk.Label(frame, text="Query 1:")
label1.grid(row=0, column=0)
entry1 = tk.Entry(frame)
entry1.grid(row=0, column=1)

label2 = tk.Label(frame, text="Query 2:")
label2.grid(row=1, column=0)
entry2 = tk.Entry(frame)
entry2.grid(row=1, column=1)

label3 = tk.Label(frame, text="Query 3:")
label3.grid(row=2, column=0)
entry3 = tk.Entry(frame)
entry3.grid(row=2, column=1)

label4 = tk.Label(frame, text="Query 4:")
label4.grid(row=3, column=0)
entry4 = tk.Entry(frame)
entry4.grid(row=3, column=1)

label5 = tk.Label(frame, text="Query 5:")
label5.grid(row=4, column=0)
entry5 = tk.Entry(frame)
entry5.grid(row=4, column=1)

search_button = tk.Button(frame, text="Search", command=search_button_click)
search_button.grid(row=5, columnspan=2, pady=10)

# Creating Table
tree_columns = ["Query 1", "Query 2", "Query 3", "Query 4", "Query 5"]
treeview = ttk.Treeview(root, columns=tree_columns, show="headings")

for col in tree_columns:
    treeview.heading(col, text=col)

treeview.pack()

root.mainloop()