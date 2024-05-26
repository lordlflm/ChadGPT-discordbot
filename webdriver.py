from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from seleniumbase import Driver

def generate_webdriver():
    try:
        driver = Driver(uc=True)
        # options = Options()
        # options.add_argument("start-maximized")
        # options.add_argument("--headless=new")
        # options.add_argument(f'--user-agent={}')
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option('useAutomationExtension', False)
        # options.add_argument('--no_sandbox')
        # options.add_argument('--disable-gpu')
        # service = Service(ChromeDriverManager().install())
        
        # driver = webdriver.Chrome(service=service, options=options)

        # stealth(driver,
        #     languages=["en-US", "en"],
        #     vendor="Google Inc.",
        #     platform="Win32",
        #     webgl_vendor="Intel Inc.",
        #     renderer="Intel Iris OpenGL Engine",
        #     fix_hairline=True,
        # )
        return driver
    except:
        #TODO manage errors better
        return None