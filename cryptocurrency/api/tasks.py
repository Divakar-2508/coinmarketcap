from celery import shared_task
from .models import Contract, Job, OfficialLink, Output, Social, Task
from coinmarketcap import CoinMarketCap
import logging

logger = logging.getLogger(__name__)

@shared_task
def fetch_cryptocurrency_data(coin_name, job_id):
    logger.info("Starting task for coin: %s, job_id: %s", coin_name, job_id)
    try:
        coin_market_cap = CoinMarketCap()
        coin_details = coin_market_cap.get_coin_details(coin_name)
        logger.info("Coin details fetched for %s: %s", coin_name, coin_details)
        
        job = Job.objects.get(job_id=job_id)
        logger.info("Job fetched: %s", job)
        
        task = Task.objects.create(job=job, coin=coin_name)
        logger.info("Task created: %s", task)
        
        output = Output.objects.create(
            task=task,
            price=coin_details["price"],
            price_change=coin_details["price_change"],
            market_cap=coin_details["market_cap"],
            market_cap_rank=coin_details["market_cap_rank"],
            volume=coin_details["volume"],
            volume_rank=coin_details["volume_rank"],
            volume_change=coin_details["volume_change"],
            circulating_supply=coin_details["circulating_supply"],
            total_supply=coin_details["total_supply"],
            diluted_market_cap=coin_details["diluted_market_cap"]
        )
        logger.info("Output created: %s", output)
        
        for contract in coin_details["contracts"]:
            Contract.objects.create(
                output=output,
                name=contract["contract_name"],
                address=contract["contract_address"]
            )
        logger.info("Contracts created for coin: %s", coin_name)
        
        for official_link in coin_details["official_links"]:
            OfficialLink.objects.create(
                output=output,
                name=official_link["name"],
                link=official_link["link"]
            )
        logger.info("Official links created for coin: %s", coin_name)
        
        for social in coin_details["socials"]:
            Social.objects.create(
                output=output,
                name=social["name"],
                url=social["url"]
            )
        logger.info("Socials created for coin: %s", coin_name)
        
        logger.info("Successfully fetched data for coin: %s", coin_name)
    except Exception as e:
        logger.error("Error fetching data for coin %s: %s", coin_name, str(e))
        raise e
