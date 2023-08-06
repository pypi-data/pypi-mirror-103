import boto3
import json


region = "us-east-1"
print("Using region:", region)

REGIONS = {}
REGION_PRICE = {}

s = boto3.Session()
all_regions = s.get_available_regions('cloudwatch')
print(all_regions)

ssm_client = boto3.client('ssm', region_name=region)

for region_id in all_regions:
    tmp = '/aws/service/global-infrastructure/regions/%s/longName' % region_id
    ssm_response = ssm_client.get_parameter(Name=tmp)
    region_name = ssm_response['Parameter']['Value']
    print("region_id:", region_id, "region_name:", region_name)

    REGIONS[region_name] = region_id


client = boto3.client('pricing')

paginator = client.get_paginator('get_products')

pages = paginator.paginate(
    ServiceCode='AmazonCloudWatch',
    Filters=[
        {
            'Field': 'ServiceCode',
            'Type': 'TERM_MATCH',
            'Value': 'AmazonCloudWatch',
        },
        {
            'Field': 'productFamily',
            'Type': 'TERM_MATCH',
            'Value': 'Storage Snapshot',
        }
    ]
)

for page in pages:
    for price in page['PriceList']:
        # print(price)
        price_json = json.loads(price)
        region = price_json["product"]["attributes"]["location"]
        term_dimension = price_json["terms"]["OnDemand"]
        price_dimensions = list(term_dimension.values())[0]["priceDimensions"]
        unit_price = list(price_dimensions.values())[0]["pricePerUnit"].get("USD")

        # Different API's export Europe differently
        region = region.replace("EU", "Europe")

        print("Resolved region price - {} - {}".format(region, unit_price))
        if region in REGIONS:
            if unit_price:
                REGION_PRICE[REGIONS[region]] = float(unit_price)
        else:
            print("Can't map '{}'".format(region))

print()
print("Final Result")
print(REGION_PRICE)