import os
import shutil
import pathlib
import time
from selenium import webdriver
from drivermanager import DriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from enum import Enum, IntEnum, auto


class Category(Enum):
    health = "health"


class Size(IntEnum):
    px16 = 1
    px32 = auto()
    px48 = auto()
    px64 = auto()
    px128 = auto()
    px256 = auto()
    px516 = auto()


class Ext(Enum):
    svg = "svg"
    jpg = "jjo"
    png = "ddo"


class Scraping_icooon_mono:
    base_url = "https://icooon-mono.com"
    health = "health"

    def __init__(self, driver_manager: DriverManager, download_path: str):
        self.dm = driver_manager
        options = self.get_options(
            # headless=headless,
            download_path=download_path
        )
        print("booting Chrome...")
        self.driver: webdriver.Chrome = webdriver.Chrome(
            executable_path=self.dm.driver_path, options=options,
        )

    def __del__(self):
        if hasattr(self, "driver"):
            self.driver.delete_all_cookies()
            self.driver.close()
            print("kill Chrome...")

    def wait_load_complete(self):
        WebDriverWait(self.driver, 60).until(
            lambda d: (d).execute_script("return document.readyState") == "complete"
        )
        time.sleep(0.5)

    def get_icon_ids(self, category: Category):
        url = f"{self.base_url}/category/{category.value}"
        self.driver.get(url)
        icon_ids = []

        next_btn_xpath = "//div[@id='wp_page_numbers']/ul/li[contains(.,'>')]/a"
        while True:
            topMaincolumn = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@id='topMaincolumn']/ul")
                )
            )
            for li in topMaincolumn.find_elements_by_tag_name("li"):
                icon_full_id: str = li.find_element_by_tag_name("span").get_attribute(
                    "data-icon"
                )
                icon_name: str = li.text
                icon_id = icon_full_id.lstrip("icon_")
                icon_ids.append((icon_id, icon_name))

            if not len(self.driver.find_elements_by_xpath(next_btn_xpath)) > 0:
                break

            self.driver.get(
                WebDriverWait(self.driver, 30)
                .until(EC.presence_of_element_located((By.XPATH, next_btn_xpath)))
                .get_attribute("href")
            )

        return icon_ids

    def get_full_icon_ids(self):
        url = f"{self.base_url}"
        self.driver.get(url)
        icon_ids = []

        next_btn_xpath = "//div[@id='wp_page_numbers']/ul/li[contains(.,'>')]/a"
        while True:
            topMaincolumn = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@id='topMaincolumn']/ul")
                )
            )
            for li in topMaincolumn.find_elements_by_tag_name("li"):
                icon_full_id: str = li.find_element_by_tag_name("span").get_attribute(
                    "data-icon"
                )
                icon_name: str = li.text
                icon_id = icon_full_id.lstrip("icon_")
                icon_ids.append((icon_id, icon_name))

            if not len(self.driver.find_elements_by_xpath(next_btn_xpath)) > 0:
                break

            self.driver.get(
                WebDriverWait(self.driver, 30)
                .until(EC.presence_of_element_located((By.XPATH, next_btn_xpath)))
                .get_attribute("href")
            )

        return icon_ids

    def download_icon(self, icon_id: str, ext: Ext, size: Size, rgb: tuple = (75,) * 3):
        url = f"{self.base_url}/{icon_id}"
        self.driver.get(url)
        self.wait_load_complete()

        size_select = self.driver.find_element_by_xpath(
            f'//ul[@id="size"]/li[{size.value}]'
        )
        self.driver.execute_script(
            "javascript:arguments[0].scrollIntoView()", size_select
        )
        size_select.click()
        color_picker = self.driver.find_element_by_xpath(
            "//input[@id='iconSingleColor']"
        )
        self.driver.execute_script(
            "javascript:arguments[0].scrollIntoView()", color_picker
        )
        color_picker.click()
        time.sleep(0.25)

        color_picker.send_keys(
            (Keys.COMMAND if self.dm.driver_os == "mac64" else Keys.CONTROL) + "a"
        )
        time.sleep(0.5)

        color_picker.send_keys(f"rgb{rgb}")
        time.sleep(1)

        self.driver.execute_script(f"javascript:{ext.value}()")

    def get_options(self, download_path: str, headless: bool = False):
        options = webdriver.ChromeOptions()

        if headless:
            print("Headless Mode")
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument(f"--window-size={480},{480}")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")

        if os.path.exists(download_path):
            raise FileExistsError(f"{download_path} は既に存在しています。削除するか、保存場所を変更してください。")
        os.mkdir(download_path)

        options.add_experimental_option(
            "prefs",
            {
                "download.prompt_for_download": False,
                "download.default_directory": download_path,
            },
        )

        return options
