import copy
import logging
import datetime
import csv
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, \
    OnSiteOrRemoteFilters

# Change root logger level (default is WARN)
logging.basicConfig(level=logging.INFO)

past_ids = []
scraped_jobs = {}
new_jobs = 0
duplicate_jobs = 0

# Read search history, store job_ids to avoid duplicates
try:
    with open('search_results.csv', 'r') as f:
        for row in csv.DictReader(f):
            past_ids.append(row['job_id'])
except:
    with open('search_results.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["job_id", "scraped_date", "query", "company", "title", "place", "posted_date",
                         "apply_link", "link"])

# Fired once for each successfully processed job
def on_data(data: EventData):
    global scraped_jobs
    global new_jobs
    global duplicate_jobs
    if data.job_id not in past_ids:
        scraped_jobs[data.job_id] = [
            # TODO change format so it can be filtered in excel
            str(datetime.datetime.now()),
            data.query,
            data.company,
            data.title,
            data.place,
            data.date,
            # data.description,
            data.apply_link,
            data.link
        ]
        # Add to past_ids just incase we get duplicates in the query results
        past_ids.append(data.job_id)
        new_jobs += 1
    else:
        duplicate_jobs += 1
    # print('[ON_DATA]', data.title, data.company, data.company_link, data.date, data.link, data.insights,
    #       len(data.description))


# Fired once for each page (25 jobs)
def on_metrics(metrics: EventMetrics):
    print('[ON_METRICS]', str(metrics))


def on_error(error):
    print('[ON_ERROR]', error)


def on_end():
    print('[ON_END]')


scraper = LinkedinScraper(
    chrome_executable_path=None,  # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver)
    chrome_binary_location=None,  # Custom path to Chrome/Chromium binary (e.g. /foo/bar/chrome-mac/Chromium.app/Contents/MacOS/Chromium)
    chrome_options=None,  # Custom Chrome options here
    headless=True,  # Overrides headless mode only if chrome_options is None
    max_workers=1,  # Setting to a single thread to avoid unsafe dictionary operations
    slow_mo=2,  # Slow down the scraper to avoid 'Too many requests 429' errors (in seconds)
    page_load_timeout=40  # Page load timeout (in seconds)
)

# Add event listeners
scraper.on(Events.DATA, on_data)
scraper.on(Events.ERROR, on_error)
scraper.on(Events.END, on_end)

queries = [
    Query(
        query='security',
        options=QueryOptions(
            locations=['United States'],
            apply_link=False,  # Try to extract apply link (easy applies are skipped). If set to True, scraping is slower because an additional page must be navigated. Default to False.
            skip_promoted_jobs=False,  # Skip promoted jobs. Default to False.
            page_offset=0,  # How many pages to skip
            limit=200,
            filters=QueryFilters(
                relevance=RelevanceFilters.RECENT,
                time=TimeFilters.WEEK,
                type=[TypeFilters.FULL_TIME, TypeFilters.CONTRACT],
                on_site_or_remote=[OnSiteOrRemoteFilters.REMOTE]
            )
        )
    ),
    Query(
        query='detection',
        options=QueryOptions(
            locations=['United States'],
            apply_link=True,  # Try to extract apply link (easy applies are skipped). If set to True, scraping is slower because an additional page must be navigated. Default to False.
            skip_promoted_jobs=False,  # Skip promoted jobs. Default to False.
            page_offset=0,  # How many pages to skip
            limit=200,
            filters=QueryFilters(
                relevance=RelevanceFilters.RECENT,
                time=TimeFilters.WEEK,
                type=[TypeFilters.FULL_TIME, TypeFilters.CONTRACT],
                on_site_or_remote=[OnSiteOrRemoteFilters.REMOTE]
            )
        )
    ),
    Query(
        query='siem',
        options=QueryOptions(
            locations=['United States'],
            apply_link=True,  # Try to extract apply link (easy applies are skipped). If set to True, scraping is slower because an additional page must be navigated. Default to False.
            skip_promoted_jobs=True,  # Skip promoted jobs. Default to False.
            page_offset=0,  # How many pages to skip
            limit=200,
            filters=QueryFilters(
                relevance=RelevanceFilters.RECENT,
                time=TimeFilters.WEEK,
                type=[TypeFilters.FULL_TIME, TypeFilters.CONTRACT],
                on_site_or_remote=[OnSiteOrRemoteFilters.REMOTE]
            )
        )
    )
]

scraper.run(queries)
for job in scraped_jobs:
    new_row = copy.deepcopy(scraped_jobs[job])
    new_row.insert(0, str(job))
    with open('search_results.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(new_row)
print(f"Duplicates skipped: {duplicate_jobs}")
print(f"New jobs added: {new_jobs}")