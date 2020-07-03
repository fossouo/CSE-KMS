import asyncio
import aioboto3
import csv
from aioboto3.s3.cse import S3CSE, KMSCryptoContext

async def main():
    ctx = KMSCryptoContext(keyid='XXX-XXXXX-XXXXX', kms_client_args={'region_name': 'us-east-1'})

#   FOR STRING ENCRYPTION 

    some_data = b'2718,CA-2011-100006,9/7/2011,9/13/2011,1,DK-13375,101,TEC-PH-10002075,377.97,1001,3,0,109.6113'

#   FOR FILES ENCRYPTION 

#   some_data = open('orders_noheaders.csv','rb')    

    async with S3CSE(crypto_context=ctx, s3_client_args={'region_name': 'us-east-1'}) as s3_cse:
        # Upload some binary data
        await s3_cse.put_object(
            Body=some_data,
            Bucket='bucketname-XXXX',
            Key='input/orders.csv.enc',
        )

        response = await s3_cse.get_object(
            Bucket='bucketname-XXXX',
            Key='input/orders.csv.enc',
        )
        data = await response['Body'].read()
        print(list(data))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
