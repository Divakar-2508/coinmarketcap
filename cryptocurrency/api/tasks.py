from celery import shared_task
from .models import Contract, Job, OfficialLink, Output, Social, Task
from coinmarketcap import CoinMarketCap

@shared_task
def fetch_cryptocurrency_data(coin_name, job_id):
    coin_market_cap = CoinMarketCap()
    coin_details = coin_market_cap.get_coin_details(coin_name)
    job = Job.objects.get(job_id=job_id)
    print("got job")
    task = Task.objects.create(job=job, coin=coin_name)
    print("task created")
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
    for contract in coin_details["contracts"]:
        Contract.objects.create(
            output=output,
            name=contract["contract_name"],
            address=contract["contract_address"]
        )
    for official_link in coin_details["official_links"]:
        OfficialLink.objects.create(
            output=output,
            name=official_link["name"],
            link=official_link["link"]
        )
    for social in coin_details["socials"]:
        Social.objects.create(
            output=output,
            name=social["name"],
            url=social["url"]
        )
