import json
import boto3
from tabulate import tabulate
import sys
import os

def gather_facts(iac_path):
    with open(iac_path, "r") as file:
        json_data = json.load(file)
    resources = json_data["resource_changes"]
    try:
        region = json_data["configuration"]["provider_config"]["aws"]["expressions"]["region"]["constant_value"]
    except KeyError as e:
        region_var = json_data["configuration"]["provider_config"]["aws"]["expressions"]["region"]["references"][0].split('.')[1]
        region = json_data["variables"]["aws_region"]["value"]
        
    list_facts = []

    for resource in range(len(resources)):
        facts = {}
        resource_type = resources[resource]["type"]
        if resource_type == "aws_instance":
            facts[resource_type] = {"class": resources[resource]["change"]["after"]["instance_type"]}
            list_facts.append(facts)

        if resource_type == "aws_db_instance":
            facts[resource_type] = {"class": resources[resource]["change"]["after"]["instance_class"], "engine": resources[resource]["change"]["after"]["engine"]}
            list_facts.append(facts)

        if resource_type == "aws_launch_configuration":
            resource_name = resources[resource]["name"]
            # print(resource_name)
            for asg_resource in resources:
                # print(asg_resource["address"])
                if resource_name in asg_resource["address"] and asg_resource["type"] == "aws_autoscaling_group":
                    desired_capacity = asg_resource["change"]["after"]["desired_capacity"]
                    # print(desired_capacity)
            while desired_capacity > 0 :
                facts[resource_type] = {"class": resources[resource]["change"]["after"]["instance_type"]}
                list_facts.append(facts)
                desired_capacity -= 1

        if resource_type == "aws_ebs_volume":
            ebs_size = resources[resource]["change"]["after"].get("size")
            ebs_type = resources[resource]["change"]["after"].get("type")
            if ebs_type is not None:
                facts[resource_type] = {"class": ebs_type, "size": ebs_size}
                list_facts.append(facts)
            if ebs_type is None:
                facts[resource_type] = {"class": "gp2", "size": ebs_size}
                list_facts.append(facts)
            
        # # if resource_type == "aws_ecs_cluster":
        # #     facts[resource_type] = {"class": resources[resource]["values"]["name"]}
        # #     list_facts.append(facts)

        if resource_type == "aws_eks_cluster":
            facts[resource_type] = {"class": resources[resource]["name"]}
            list_facts.append(facts)

    return list_facts, region

def query_cost(filters, resource_type):
    service_codes = {
        "aws_instance": "AmazonEC2",
        "aws_db_instance": "AmazonRDS",
        # "aws_ecs_cluster": "AmazonECS",
        "aws_eks_cluster": "AmazonEKS",
        "aws_launch_configuration": "AmazonEC2",
        "aws_ebs_volume": "AmazonEC2"
    }
    # print(resource_type)
    cost_usd = None
    ServiceCode = service_codes.get(resource_type)
    # print(f"{ServiceCode} {resource_type} {filters}")
    response = client.get_products(
    ServiceCode = ServiceCode,
    Filters= filters,
    FormatVersion='aws_v1'
    # MaxResults=1
    )
    price_data = response['PriceList']

    if ServiceCode == "AmazonEC2" or ServiceCode == "AmazonRDS":
        for resource in price_data:
            json_data = json.loads(resource)
            # print(json_data)
            for value in json_data["terms"]["OnDemand"].values():
                for price_value in value["priceDimensions"].values():
                    if float(price_value["pricePerUnit"]["USD"]) > 0:
                        cost_usd = price_value["pricePerUnit"]["USD"]
                        break
                if cost_usd is not None:
                    break
            if cost_usd is not None:
                break
        return cost_usd, ServiceCode + "/" + resource_type

    if ServiceCode == "AmazonEKS":
        for resource in price_data:
            json_data = json.loads(resource)
            # print(json_data)
            if "AmazonEKS-Hours:perCluster" in json_data["product"]["attributes"]["usagetype"]:
                for value in json_data["terms"]["OnDemand"].values():
                    for price_value in value["priceDimensions"].values():
                        if float(price_value["pricePerUnit"]["USD"]) > 0:
                            cost_usd = price_value["pricePerUnit"]["USD"]
                            break
                    if cost_usd is not None:
                        break
                if cost_usd is not None:
                    break
        return cost_usd, ServiceCode + "/" + resource_type

def filter_resource(facts):
    tabulate_cost = []
    total_hourly = 0
    total_monthly = 0
    for fact in facts:
        for resource_type, meta_data in fact.items():
            
            if resource_type == "aws_db_instance":
                filters = [
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'databaseEngine',
                    'Value': meta_data["engine"]
                },
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'instanceType',
                    'Value': meta_data["class"]
                },
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'regionCode',
                    'Value': region,
                },
                {   'Type': 'TERM_MATCH',
                    'Field': 'deploymentOption',
                    'Value': "Single-AZ",
                },
                ]
            
            if resource_type == "aws_ecs_cluster":
                filters = [
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'group',
                    'Value': meta_data["class"]
                },
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'location',
                    'Value': region 
                }
                ]

            if resource_type == "aws_eks_cluster":
                filters =  [
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'productFamily',
                    'Value': 'Compute'
                },
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'regionCode',
                    'Value': region
                }
                ]
            
            if resource_type == "aws_instance":
                filters = [
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'instanceType',
                    'Value': meta_data["class"]
                },
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'regionCode',
                    'Value': region,
                },
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'operatingSystem',
                    'Value': 'Linux',
                },
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'preInstalledSw',
                    'Value': 'NA',
                },
                ]

            if resource_type == "aws_launch_configuration":
                filters = [
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'instanceType',
                    'Value': meta_data["class"]
                },
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'regionCode',
                    'Value': region,
                },
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'operatingSystem',
                    'Value': 'Linux',
                },
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'preInstalledSw',
                    'Value': 'NA',
                },
                ]

            if resource_type == "aws_ebs_volume":
                filters = [
                {
                'Type': 'TERM_MATCH',
                'Field': 'productFamily',
                'Value': 'Storage'
                },
                {
                'Type': 'TERM_MATCH',
                'Field': 'regionCode',
                'Value': region  # Your desired region, e.g., 'us-east-1'
                },
                {
                'Type': 'TERM_MATCH',
                'Field': 'volumeApiName',
                'Value': meta_data["class"]  # Replace 'gp2' with your desired EBS volume type
                }
                ]
        # print(filters)
        cost_usd, resource_type = query_cost(filters, resource_type)
        # print(cost_usd, resource_type, meta_data["class"], meta_data.get("size"))
        if meta_data.get("size") is not None:
            tabulate_cost.append([resource_type, meta_data["class"] + "/" + str(meta_data.get("size")) + " GB", str(float(cost_usd)) + " USD", "{:.2f}".format(float(cost_usd)*(meta_data.get("size"))) + " USD"])
        else:
            tabulate_cost.append([resource_type, meta_data["class"], str(float(cost_usd)) + " USD", "{:.2f}".format(float(cost_usd)*(30.42*24)) + " USD"])
            
    total_hourly = str("{:.2f}".format(float(sum(float(row[2].split()[0]) for row in tabulate_cost))))+ " USD"
    total_monthly = str(float(sum(float(row[3].split()[0]) for row in tabulate_cost))) + " USD"
    tabulate_cost.extend([["------Total Cost------", "", total_hourly, total_monthly]])

    return tabulate_cost


iac_path = os.path.join(os.environ.get("GITHUB_WORKSPACE"), os.environ.get("IAC_PATH"), "tfplan.json")
# print(iac_path)
# terraform_command = ['terraform', 'show', '-json', 'tfplan.binary']


# try:
#     result = subprocess.run(terraform_command, cwd=iac_path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
#     output = result.stdout
#     with open(iac_path + "/" + "tfplan.json", "w") as file:
#         file.write(output)
#     print(iac_path + "/" + "tfplan.json")
# except subprocess.CalledProcessError as e:
#     print(f"Error running command: {e}")

# with open(iac_path + "/" + "tfplan.json", "r") as file:
#     json_data = file.read()
# print(json_data)

# with open(iac_path + "/" + "tfplan.json", "r") as file:
#     content = json.load(file)
# print(content)

facts, region = gather_facts(iac_path)
client = boto3.client("pricing", region_name="us-east-1")
# print(facts)
tabulate_cost = filter_resource(facts)
# print(tabulate_cost)
headers = ["Service Name", "Instance Class", "Hourly Cost", "Monthly Cost"]
alignments = ["left", "left", "right", "right"]
print("-" * 30)
print("Cost Predict Output:")
print("+------------------------------------+----------------+-------------+--------------+")
print(tabulate(tabulate_cost, headers=headers, tablefmt="pretty", colalign=alignments))
print("+------------------------------------+----------------+-------------+--------------+")

