from seleniumbase import Driver
import sqlite3
import time

def scrape_rozee(driver):
    jobs = []
    for page in range(1, 3):  # 2 pages for Rozee
        driver.get(f"https://www.rozee.pk/job/jsearch/q/all/pn/{page}")
        time.sleep(3)
        cards = driver.find_elements("css selector", ".job")

        for card in cards:
            try:
                title = card.find_element("css selector", ".job-title").text.strip()
            except:
                title = "N/A"
            try:
                company = card.find_element("css selector", ".company-name").text.strip()
            except:
                company = "N/A"
            try:
                location = card.find_element("css selector", ".job-location").text.strip()
            except:
                location = "N/A"
            try:
                skills = card.find_element("css selector", ".skills").text.strip()
            except:
                skills = "N/A"
            try:
                date = card.find_element("css selector", ".date").text.strip()
            except:
                date = "N/A"

            jobs.append((title, company, location, skills, date, "Rozee.pk"))
    return jobs

def scrape_indeed(driver):
    jobs = []
    for page in range(0, 20, 10):  # 2 pages for Indeed
        driver.get(f"https://www.indeed.com/jobs?q=software+developer&start={page}")
        time.sleep(3)
        cards = driver.find_elements("css selector", "div.job_seen_beacon")

        for card in cards:
            try:
                title = card.find_element("css selector", "h2.jobTitle").text.strip()
            except:
                title = "N/A"
            try:
                company = card.find_element("css selector", "span.companyName").text.strip()
            except:
                company = "N/A"
            try:
                location = card.find_element("css selector", "div.companyLocation").text.strip()
            except:
                location = "N/A"
            skills = "N/A"
            try:
                date = card.find_element("css selector", "span.date").text.strip()
            except:
                date = "N/A"

            jobs.append((title, company, location, skills, date, "Indeed.com"))
    return jobs

def save_to_db(jobs):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS jobs')
    c.execute('''
        CREATE TABLE jobs (
            title TEXT, company TEXT,
            location TEXT, skills TEXT,
            date_posted TEXT, source TEXT
        )
    ''')
    c.executemany('INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?)', jobs)
    conn.commit()
    conn.close()

def scrape_jobs():
    driver = Driver(headless=True)
    try:
        rozee_jobs = scrape_rozee(driver)
        indeed_jobs = scrape_indeed(driver)
        all_jobs = rozee_jobs + indeed_jobs
        save_to_db(all_jobs)
        print(f"✅ Scraped {len(all_jobs)} jobs and saved to jobs.db")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_jobs()
