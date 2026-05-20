
# LinkedIn Job & Personnel Scraper

A Python-based basic scraper for extracting LinkedIn job listings and associated personnel/company information.  
Designed for recruitment analytics, talent discovery, hiring intelligence, and labor market research workflows.

## Features

- Scrape LinkedIn job listings
- Extract:
  - Job title
  - Company name
  - Location
  - Job description
  - Skills/keywords
- Fetch associated personnel/company employee data
- Export results to:
  - CSV

---

## Tech Stack

- Python
- Playwright

---

## Installation

```bash
git clone https://github.com/yourusername/linkedin-job-scraper.git
cd linkedin-job-scraper

python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
````

---

## Usage

### Scrape Job Listings

```bash
python scrapejobsandpeople.py \
  --query "Machine Learning Engineer" 
```

### Fetch Personnel Information

```bash
python scarppl.py
```

The scraper stops for personal intervention at 15-20 steps to avoid being blocked by LinkedIN.
This script goes through the scraped people from scrapejobsandpeople.py script and gets more information to create a prompt for reaching out.

---


### Get Prompt for reaching out

```bash
python get_prompt.py <linkedin_profile_for_person>
```
This script scrapes the personal details for the attached person, generates a prompt to get a reaching out message and pastes to the clipboard. It can be used in chatgpt or gemini to get the message to send.

---

## Data Export

Supported formats:

* CSV


---

## Disclaimer

This project is intended for educational and research purposes only.

Users are responsible for complying with:

* LinkedIn Terms of Service
* Applicable data privacy laws
* Rate limiting and ethical scraping practices

Do not use this project for spam, abuse, or unauthorized data harvesting.

---

## Future Improvements

* Captcha solving integration
* Distributed scraping workers
* AI-powered job classification
* Semantic candidate-job matching
* Web dashboard
* Resume enrichment pipeline
