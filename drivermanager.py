import platform
import os


class DriverManager:
    def __init__(self, driver_dir, driver_version):
        self.driver_dir = os.path.abspath(driver_dir)
        self.driver_ver = driver_version
        self.driver_os, self.driver_name = self.getDriverOS()
        self.driver_path = os.path.join(
            self.driver_dir,
            "driver",
            self.driver_ver,
            self.driver_os,
            self.driver_name,
        )

    def getDriverOS(self) -> str:
        platform_name = platform.system()
        if platform_name == "Windows":
            return "win32", "chromedriver.exe"
        elif platform_name == "Darwin":
            return "mac64", "chromedriver"
        else:
            return "linux64", "chromedriver"