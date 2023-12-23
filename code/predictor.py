import boto3
import json

# client = boto3.client('pricing', region_name='us-east-1')

# response = client.get_products(
#     ServiceCode='AmazonEC2',
#     Filters=[
#         {
#             'Type': 'TERM_MATCH',
#             'Field': 'instanceType',
#             'Value': 't2.micro',
#         },
#         {
#             'Type': 'TERM_MATCH',
#             'Field': 'regionCode',
#             'Value': 'us-east-1',
#         },
#         {
#             'Type': 'TERM_MATCH',
#             'Field': 'operatingSystem',
#             'Value': 'Linux',
#         },
#         {
#             'Type': 'TERM_MATCH',
#             'Field': 'preInstalledSw',
#             'Value': 'NA',
#         },
#     ],
#     FormatVersion='aws_v1',
#     # MaxResults=1
# )
# price_data = response['PriceList']


# cost_usd = None
# for resource in price_data:
#     json_data = json.loads(resource)
#     # print(json_data)
#     for key, value in json_data["terms"]["OnDemand"].items():
#         for price_k, price_v in value["priceDimensions"].items():
#             if float(price_v["pricePerUnit"]["USD"]) > 0:
#                 cost_usd = (price_v["pricePerUnit"]["USD"])
#                 break
#         if cost_usd is not None:
#             break
#     if cost_usd is not None:
#         break
# print(cost_usd)
# response = client.get_products(
#     ServiceCode='AmazonRDS',
#     Filters=[
#                 {
#                     'Type': 'TERM_MATCH',
#                     'Field': 'databaseEngine',
#                     'Value': "mysql"
#                 },
#                 {
#                     'Type': 'TERM_MATCH',
#                     'Field': 'instanceType',
#                     'Value': "db.t2.micro"
#                 },
#                 {
#                     'Type': 'TERM_MATCH',
#                     'Field': 'regionCode',
#                     'Value': "us-east-1",
#                 },
#                 {    'Type': 'TERM_MATCH',
#                     'Field': 'deploymentOption',
#                     'Value': "Single-AZ",
#                 },
#                 ],
#     FormatVersion='aws_v1',
#     # MaxResults=1
# )
# price_data = response['PriceList']
# for resource in price_data:
#     print(resource)
#     json_data = json.loads(resource)
#     for key, value in json_data["terms"]["OnDemand"].items():
#         for price_k, price_v in value["priceDimensions"].items():
#             print(price_v["pricePerUnit"]["USD"])
    



# response = client.get_products(
#     ServiceCode='AWSElasticIP',
#     Filters=[

#         {
#             'Type': 'TERM_MATCH',
#             'Field': 'regionCode',
#             'Value': 'us-east-1'
#         }
#     ],
#     FormatVersion='aws_v1',
#     # MaxResults=1
# )
# price_data = response['PriceList']

# print(price_data)
# for resource in price_data:
#     json_data = json.loads(resource)
#     print(json_data["product"]["attributes"]["usagetype"])
#     if json_data["product"]["attributes"]["usagetype"] == "USE1-AmazonEKS-Hours:perCluster":
#         for key, value in json_data["terms"]["OnDemand"].items():
#             for price_key, price_value in value["priceDimensions"].items():
#                 print(price_value["pricePerUnit"]["USD"])
         
# import boto3

# def get_ebs_cost(region, volume_size_gb):
#     client = boto3.client('pricing', region_name=region)
    
#     response = client.get_products(
#         ServiceCode='AmazonEC2',
#         Filters=[
#             {
#                 'Type': 'TERM_MATCH',
#                 'Field': 'productFamily',
#                 'Value': 'Storage'
#             },
#             {
#                 'Type': 'TERM_MATCH',
#                 'Field': 'regionCode',
#                 'Value': region  # Your desired region, e.g., 'us-east-1'
#             },
#             {
#                 'Type': 'TERM_MATCH',
#                 'Field': 'volumeApiName',
#                 'Value': 'gp3'  # Replace 'gp2' with your desired EBS volume type
#             }
#             # {
#             #     'Type': 'TERM_MATCH',
#             #     'Field': 'volumeSize',
#             #     'Value': str(volume_size_gb)  # Specify the volume size in GB
#             # }
#         ],
#         FormatVersion='aws_v1'
#     )
#     # print(response["PriceList"])
#     for resource in response["PriceList"]:
#         print(json.loads(resource))
#     # return response

# # Example usage for a 100GB volume in us-east-1 region:
# region = 'us-east-1'
# volume_size = 100
# ebs_cost = get_ebs_cost(region, volume_size)
# print(ebs_cost)

tabulate_cost = [['AmazonRDS/aws_db_instance', 'db.t2.micro', '0.017 USD', '12.41 USD'], ['AmazonEC2/aws_ebs_volume', 'gp3/50 GB', '0.08 USD', '4.00 USD'], ['AmazonEC2/aws_ebs_volume', 'gp2/10 GB', '0.1 USD', '1.00 USD'], ['AmazonEKS/aws_eks_cluster', 'my-eks-cluster', '0.1 USD', '73.01 USD'], ['AmazonEC2/aws_instance', 'm5.large', '0.096 USD', '70.09 USD'], ['AmazonEC2/aws_instance', 't2.micro', '0.0116 USD', '8.47 USD'], ['AmazonEC2/aws_launch_configuration', 'm7g.large', '0.0867 USD', '63.30 USD'], ['AmazonEC2/aws_launch_configuration', 'm7g.large', '0.0867 USD', '63.30 USD']]
total = 0
# for row in tabulate_cost:
#     total += float(row[2].split()[0])
# print(total)
total = sum(float(row[2].split()[0]) for row in tabulate_cost)

print(total)