import yaml

from ig_markets.rest_client import IGRestClient
import ig_markets.stream_client as igls

#stream = file('demo.yaml', 'r')
#config = yaml.load(stream)
# Tell the user when the Lighstreamer connection state changes
def on_state(state):
    print 'New state:', state
    igls.LOG.debug('New state: ' + str(state))
    
#ig_service = IGRestClient('lthams',
#                          '1q2w3e4rT',
#                          '4b5b2858a447c9f5bd879b6876da9e0be3878b4d',
#                          'https://demo-api.ig.com/gateway/deal')

client = igls.IGLsClient()
client.on_state.listen(on_state)
account_id = client.create_session(username='lthams',
                                   password='1q2w3e4rT',
                                   api_url='https://demo-api.ig.com/gateway/deal',
                                   api_key='4b5b2858a447c9f5bd879b6876da9e0be3878b4d'
                                  )

priceTable = igls.Table(client,
                        mode=igls.MODE_MERGE,
                        item_ids='L1:CS.D.EURUSD.CFD.IP',
                        schema='UPDATE_TIME BID OFFER CHANGE CHANGE_PCT MARKET_STATE',
                        item_factory=lambda row: tuple(float(v) for v in row))

priceTable.on_update.listen(processPriceUpdate)

priceTable = igls.Table(client,
                        mode=igls.MODE_MERGE,
                        item_ids='L1:IX.D.DAX.IMF.IP',
                        schema='UPDATE_TIME BID OFFER CHANGE CHANGE_PCT MARKET_STATE',
                        item_factory=lambda row: tuple(float(v) for v in row))

priceTable.on_update.listen(processPriceUpdate)

balanceTable = igls.Table(client,
                          mode=igls.MODE_MERGE,
                          item_ids='ACCOUNT:' + account_id,
                          schema='PNL DEPOSIT AVAILABLE_CASH',
                          item_factory=lambda row: tuple(str(v) for v in row))

balanceTable.on_update.listen(processBalanceUpdate)

while True:
    time.sleep(10)
