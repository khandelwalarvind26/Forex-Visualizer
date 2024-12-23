from app.utils import QuoteDataEnum, logger
from app.db import Quote, get_db

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

from datetime import datetime
import traceback, time, os

class Scraper:
    

    def __init__(self):  
        '''Initialize with countries and dates'''

        self.countries = None
        self.quotes = None
        self.driver = self.get_driver()
    

    async def save(self):
        '''Save the quotes scraped into sqlite DB'''
        
        try:
            async for db in get_db():
                db.add_all(self.quotes)
                await db.commit()

        except Exception as _:
            tb = traceback.format_exc()
            logger.info(tb)


    def scrape(self, from_country: str, to_country: str, from_date: datetime, to_date: datetime):
        '''Fetch all quotes wihtin the specified dates'''

        try:
            # Convert datetime values to integer timestamps
            timestamps = (int(from_date.timestamp()), int(to_date.timestamp()))
            self.countries = (from_country, to_country)

            # Build url
            url = f"https://finance.yahoo.com/quote/{self.countries[0]}{self.countries[1]}%3DX/history/?period1={timestamps[0]}&period2={timestamps[1]}"
            

            page_source = self.get_page_source(url)
            self.quotes = self.parse_page_source(page_source)

        except Exception as _:
            tb = traceback.format_exc()
            logger.info(tb)


    def get_page_source(self, url: str):
        '''Function to fetch the entire source html given the url'''
        try: 

            time1 = datetime.now()
            logger.info("Driver started")

            # Load web page from url
            self.driver.get(url) # tells selenium to load url on chrome driver

            # Wait for 5 seconds before closing the web page, irresepective of load status
            time.sleep(5) 

            time2 = datetime.now()
            logger.info(f"Done loading web page, Total time taken: {(time2 - time1).total_seconds()}")

            # Fetch full html source of current page
            return self.driver.page_source
        
        except Exception as e:
            tb = traceback.format_exc()
            logger.info(tb)


    def parse_page_source(self, page_source):
        '''Take html source as input and return a List of Quote objects'''

        # Load the source html code into beautiful soup
        soup = BeautifulSoup(page_source,'html.parser')

        # Find the table-container div on the page
        table_container = soup.find('div', class_='table-container')

        # Find the table inside table container
        table = table_container.find('table', class_='table')

        # Extract the table header
        thead = table.find('thead')

        # Extract all tbody elements (since there are multiple)
        tbody = table.find('tbody')

        # Extract all the rows of the table
        trows = tbody.find_all('tr')
        
        quotes = []

        # Iterate through each row and access the data
        for trow in trows:
            quote_data = trow.find_all('td')
            quote = self.parse_quote_data(quote_data)
            quotes.append(quote)
        
        return quotes


    def parse_quote_data(self, quote_data: list) :
        '''Input quote_data in list form -> return Quote object'''

        return Quote(
            date = self.parse_date(quote_data[QuoteDataEnum.date.value].get_text()), 
            open = float(quote_data[QuoteDataEnum.open.value].get_text()),
            high = float(quote_data[QuoteDataEnum.high.value].get_text()),
            low = float(quote_data[QuoteDataEnum.low.value].get_text()),
            close = float(quote_data[QuoteDataEnum.close.value].get_text()),
            adj_close = float(quote_data[QuoteDataEnum.adj_close.value].get_text()),
            from_country = self.countries[0],
            to_country = self.countries[1],
        )


    # Given date string from yahoo forex site, convert it into datetime object
    def parse_date(self, date_string: str) :
        '''Given date string from yahoo forex site, convert it into datetime object'''
        
        date_object = datetime.strptime(date_string, "%b %d, %Y")
        return date_object


    def get_driver(self):
        '''Get chrome driver'''
        try: 
            
            chrome_options = Options()
            prefs = {
                "profile.managed_default_content_settings.images": 2,  # Disable images
                "profile.managed_default_content_settings.stylesheets": 2,  # Disable CSS
                "profile.managed_default_content_settings.fonts": 2,  # Disable fonts
            }
            chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox") 
            chrome_options.add_argument("--disable-dev-shm-usage") 
            chrome_options.add_argument("--disable-gpu") # Disable GPU rendering
            chrome_options.add_argument("--window-size=1920,1080") # Fixed window size
            chrome_options.add_argument("--disable-logging")  # Disable Selenium logging
            chrome_options.add_argument("--log-level=3")     # Set Chrome log level to FATAL
            chrome_options.page_load_strategy = "none"
            
            # Get chromedriver path
            chromedriver_path = ChromeDriverManager().install()

            # If wrong path fix it
            if 'THIRD_PARTY_NOTICES.chromedriver' in chromedriver_path:
                chromedriver_path = chromedriver_path.replace('THIRD_PARTY_NOTICES.chromedriver', 'chromedriver')
            logger.info(chromedriver_path)

            # Make path executable
            os.chmod(chromedriver_path, 0o755)

            # Get the service
            service = Service(chromedriver_path)

            # Get driver
            driver = webdriver.Chrome(service=service, options=chrome_options)

            return driver
        
        except Exception as _:
            tb = traceback.format_exc()
            logger.info(tb)

    
    # Destructor, quit driver
    def __del__(self):
        # if self.driver is not None:
        self.driver.quit()