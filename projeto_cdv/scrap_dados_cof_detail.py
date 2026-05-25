## Scrap dos dados para projeto cdv

#href="https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/restricao_coff_eolica_detail_tm/RESTRICAO_COFF_EOLICA_DETAIL_2026_05.csv"


# mes_atual - 6 == "..._202X_XX"

import requests 
import sys
from datetime import date
from dateutil.relativedelta import relativedelta


url_base = "https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/restricao_coff_eolica_detail_tm/"

date_obj = date(2026,3,1) # We can use date.today for normal usage

if len(sys.argv) < 2:
    n_month_available = 6
else:
    n_month_available = int(sys.argv[1])


for m in range(n_month_available):
    month = (date_obj - relativedelta(months = m)).month
    year = (date_obj - relativedelta(months = m)).year

    filename = "RESTRICAO_COFF_EOLICA_DETAIL_" + f"{year}_{month:02d}.csv"

    url = url_base + filename
    response = requests.get(url)

    if response.status_code == 200:
        with open(f"/home/pcleonardo/projeto_cdv/dados_restrição_detalhamento_SPEs/{filename}", "wb") as f:
            f.write(response.content)
            print(f"{filename} - Download complete")
