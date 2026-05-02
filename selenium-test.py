from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

try:
    driver.get("http://10.48.229.161:32000")
    assert "CIT225" in driver.title or "CI/CD" in driver.page_source, \
        "Page content not found — acceptance test FAILED"
    print("Acceptance test PASSED:", driver.title)
finally:
    driver.quit()
