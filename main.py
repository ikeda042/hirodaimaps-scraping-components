from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import asyncio


class Navitime:
    def __init__(self) -> None:
        self.url = "https://www.navitime.co.jp/bus/diagram/timelist?departure=00026254&arrival=00026237&line=00024433"
        self.driver_path = "./chromedriver"
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.service = Service(executable_path=self.driver_path)

    @staticmethod
    def parse_time_detail(html_source: str) -> list[list[str]]:
        bs = BeautifulSoup(html_source, "html.parser")
        time_details = bs.find_all("ul", class_="time-detail")
        return [
            [
                time_detail.find("span", class_="time dep").text,
                time_detail.find("span", class_="time arr").text,
            ]
            for time_detail in time_details
        ]

    async def request(self) -> None:
        with webdriver.Chrome(
            service=self.service, options=self.chrome_options
        ) as driver:
            driver.get(self.url)

            driver.set_window_size(900, 1000)
            driver.execute_script("document.body.style.zoom='50%'")
            wait = WebDriverWait(driver, 0)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            self.html_source = driver.page_source
            time_details = self.parse_time_detail(self.html_source)
            print(time_details)


if __name__ == "__main__":
    navitime = Navitime()
    asyncio.run(navitime.request())
