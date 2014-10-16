import webapp2
from src.settings import JINJA_ENVIRONMENT
from src.my_storage import Storage
import requests
import datetime
import json
import logging


class Index(webapp2.RequestHandler):
    def get(self):
        template_values = {
        }
        template = JINJA_ENVIRONMENT.get_template('main/templates/index.html')
        self.response.write(template.render(template_values))


class ScrapeOanda(webapp2.RequestHandler):
    def get(self):
        # get oanda data
        currencies = [
            'AUD_USD',
            'EUR_GBP',
            'EUR_JPY',
            'EUR_USD',
            'GBP_USD',
            'GBP_JPY',
            'NZD_USD',
            'USD_CAD',
            'USD_CHF',
            'USD_JPY',
        ]
        period = 3600
        for currency in currencies:
            tries = 0
            while tries < 5:
                tries += 1
                url = 'https://api-fxpractice.oanda.com/labs/v1/orderbook_data?instrument={0}&period={1}'.format(currency, period)
                headers = {'Authorization': 'Bearer e784eb5916aff0cef1e40384f91efcbc-894f13baacee725fe3294136ac8fa469'}
                res = requests.get(url, headers=headers)
                resText = json.loads(res.text)
                if 'code' not in resText:
                    break
                else:
                    logging.warn('Error received in response: {0}'.format(resText['message']))
            # raise Exception(res.text)

            # save to storage
            gcs = Storage()
            gcs.createFile(
                filename='/' + currency.replace('_', '') + '/' + datetime.datetime.now().strftime("%y-%m-%d-%H-%M") + '.json',
                data=res.text,
            )
