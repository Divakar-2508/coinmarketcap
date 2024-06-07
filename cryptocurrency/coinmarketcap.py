import os
import dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class CoinMarketCap():
    def __init__(self):
        dotenv.load_dotenv()
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
    
    def make_request(self, coin: str):
        url = os.getenv("SCRAP_URL") + coin
        self.driver.get(url)
    
    def get_coin_details(self, coin: str) -> dict[str, any]:
        self.make_request(coin)

        price = self.driver.find_element(
            "xpath",
            os.getenv("PRICE_XPATH")
        ).text.lstrip("$")
        price = float(price)
        
        price_change = self.driver.find_element(
            "xpath",
            os.getenv("PRICE_CHANGE_XPATH")
        )
        price_change_sign = '-' if price_change.get_attribute("color").lower() == "red" else '+'
        price_change = float(price_change_sign + price_change.text.split("%")[0])

        market_cap = self.driver.find_element(
            By.XPATH,
            os.getenv("MARKET_CAP_XPATH")
        ).text.splitlines()[1].lstrip("$").replace(",", "")
        market_cap = float(market_cap)

        market_cap_rank = self.driver.find_element(
            By.XPATH,
            os.getenv("MARKET_CAP_RANK_XPATH")
        ).text.lstrip("#")
        market_cap_rank = int(market_cap_rank)

        volume = self.driver.find_element(
            By.XPATH,
            os.getenv("VOLUME_XPATH")
        ).text.splitlines()[1].lstrip("$").replace(",", "")
        volume = float(volume)

        volume_rank = self.driver.find_element(
            By.XPATH,
            os.getenv("VOLUME_RANK_XPATH")
        ).text.lstrip("#")
        volume_rank = int(volume_rank)
        
        volume_change = self.driver.find_element(
            By.XPATH,
            os.getenv("VOLUME_CHANGE_XPATH")
        ).text.rstrip("%")
        volume_change = float(volume_change)

        circulating_supply = self.driver.find_element(
            By.XPATH,
            os.getenv("CIRCULATING_SUPPLY_XPATH")
        ).text.split(" ")[0].replace(",", "")
        circulating_supply = int(circulating_supply)

        total_supply = self.driver.find_element(
            By.XPATH,
            os.getenv("TOTAL_SUPPLY_XPATH")
        ).text.split(" ")[0].replace(",", "")
        total_supply = int(total_supply)

        diluted_market_cap = self.driver.find_element(
            By.XPATH,
            os.getenv("DILUTED_MARKET_CAP_XPATH")
        ).text.lstrip("$").replace(",", "")
        diluted_market_cap = int(diluted_market_cap)

        contracts_div = self.driver.find_element(
            By.XPATH,
            os.getenv("CONTRACTS_XPATH")
        )

        contracts_ele = contracts_div.find_elements(By.CLASS_NAME, "chain-name")
        contracts = []
        for contract in contracts_ele:
            contract_name = contract.text.splitlines()[0].rstrip(" :")
            contract_address = contract.get_attribute("href").split("/")[-1]
            contracts.append({
                "contract_name": contract_name,
                "contract_address": contract_address
            })
        
        official_links_div = self.driver.find_element(
            By.XPATH,
            os.getenv("OFFICIAL_LINKS_XPATH")
        )
        official_link_eles = official_links_div.find_elements(By.TAG_NAME, "a")
        official_links = []
        for official_link in official_link_eles:
            link_name = official_link.text
            link = official_link.get_attribute("href")
            official_links.append({
                "name": link_name,
                "link": link
            })
        
        socials_div = self.driver.find_element(
            By.XPATH,
            os.getenv("SOCIALS_XPATH")
        )
        social_eles = socials_div.find_elements(By.TAG_NAME, "a")
        socials = []
        for social in social_eles:
            social_name = social.text
            if len(social_name.splitlines()) > 1:
                social_name = social_name.splitlines()[1]
            social_url = social.get_attribute("href")
            socials.append({
                "name": social_name,
                "url": social_url
            })

        return {
            "price": price,
            "price_change": price_change,
            "market_cap": market_cap,
            "market_cap_rank": market_cap_rank,
            "volume": volume,
            "volume_rank": volume_rank,
            "volume_change": volume_change,
            "circulating_supply": circulating_supply,
            "total_supply": total_supply,
            "diluted_market_cap": diluted_market_cap,
            "contracts": contracts,
            "official_links": official_links,
            "socials": socials
        }

# app = CoinMarketCap()
# app.get_coin_details("duko")