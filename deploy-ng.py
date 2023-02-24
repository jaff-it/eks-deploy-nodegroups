import boto3
import argparse
import yaml
import re


def update_ng():
    client = boto3.client('eks')

    response = client.update_nodegroup_config(
        clusterName=cluster,
        nodegroupName=name,
        labels={
            'addOrUpdateLabels': labels,
        },
        scalingConfig={
            'minSize': int(min_size),
            'maxSize': int(max_size),
            'desiredSize': int(desired)
        },
        updateConfig={
            'maxUnavailablePercentage': 20
        },
    )

def create_ng():
    client = boto3.client('eks')

    response = client.create_nodegroup(
        clusterName=cluster,
        nodegroupName=name,
        scalingConfig={
            'minSize': int(min_size),
            'maxSize': int(max_size),
            'desiredSize': int(desired)
        },

        subnets=list_subnets,
        instanceTypes=list_instance_types,
        amiType=ami_type,

        nodeRole=node_role,
        labels=labels,

        launchTemplate={
            'id': launch_template
        },
        updateConfig={
            'maxUnavailablePercentage': 20
        },
        capacityType=capacity_type,
    )



## Parse arguments

parser = argparse.ArgumentParser(description='Create EKS node group')

parser.add_argument('--config-file', dest="config_file",
                    help='Configuration file')

parser.add_argument('--cluster', dest="cluster",
                    help='Cluster name')
parser.add_argument('-n', '--name', dest="name",
                    help='Node group name')
parser.add_argument('-l', '--lifecycle', dest="lifecycle",
                    help='spot or on-demand')
parser.add_argument('-s', '--list-subnets', dest="list_subnets", nargs='+', default=[],
                    help='List of subnets (--list-subnets subnet-id-1  subnet-id-2)')
parser.add_argument('-t', '--list-instance-types', dest="list_instance_types", nargs='+', default=[],
                    help='List of instance types (--list-instance-types r5.xlarge r5a.xlarge)')
parser.add_argument('-L', '--launch-template', dest="launch_template",
                    help='Launch template id')
parser.add_argument('--min', dest="min_size", default=0,
                    help='Min size, default = 0')
parser.add_argument('--max', dest="max_size",
                    help='Max size')
parser.add_argument('--desired', dest="desired",
                    help='Desired size')
parser.add_argument('--labels', dest="labels", nargs='+',
                    help='Labels (--labels "\'environment\': \'develop\', \'proj\': \'my-project\'")')
parser.add_argument('--node-role', dest="node_role",
                    help='Node Role ARN (--node-role "arn:aws:iam::<ACCOUNT>:role/<EKS_Managment_Role>")')
parser.add_argument('--ami-type', dest="ami_type",
                    help='AMI type (--ami-type "AL2_x86_64")')

args = parser.parse_args()
list_ng = []

if args.config_file == None:
    cluster = args.cluster
    print("Cluster name: ", args.cluster)
    name = args.name
    print("Node group name: ", args.name)
    list_subnets = args.list_subnets
    print("List of subnets: ", args.list_subnets)
    list_instance_types = args.list_instance_types
    print("List of instance types: ", args.list_instance_types)
    launch_template = args.launch_template
    print("Launch template id: ", args.launch_template)
    if args.lifecycle == 'spot':
        lifecycle = 'Ec2Spot'
        capacity_type = 'SPOT'
    elif args.lifecycle == 'on-demand':
        lifecycle = 'OnDemand'
        capacity_type = 'ON_DEMAND'
    print("Lifecycle: ", lifecycle, " capacity_type: ", capacity_type)
    min_size = args.min_size
    max_size = args.max_size
    desired = args.desired
    print("Min size: ", args.min_size, "   Max size: ", args.max_size, "   Desired size: ", args.desired)

    labels = args.labels[0]
    print("Kubernetes labels: ", labels)
    node_role = args.node_role

    client = boto3.client('eks')
    list_ng = client.list_nodegroups(clusterName=cluster)["nodegroups"]

    if name in list_ng:
        print("Node Group exists, will be updated")
        confirm = input(" CONFIRM EXECUTION? (yes / No): ")
        if confirm == 'yes':
            update_ng()
        else:
            print("EXIT")
            exit()
    else:
        print("Node Group does not exists, will be created")
        confirm = input(" CONFIRM EXECUTION? (yes / No): ")
        if confirm == 'yes':
            create_ng()
        else:
            print("EXIT")
            exit()


if args.config_file != None:
    yaml.warnings({'YAMLLoadWarning': False})
    with open(args.config_file, "r") as ymlfile:
        cfg = yaml.full_load(ymlfile.read().replace('\t', ' '))

    if args.cluster == None:
        cluster = cfg["metadata"]["name"]
    else:
        cluster = args.cluster

    client = boto3.client('eks')
    list_ng = client.list_nodegroups(clusterName=cluster)["nodegroups"]

    for ng in range(0, len(cfg["managedNodeGroups"])):
        print("")
        print("")
        if args.name == None:
            name = cfg["managedNodeGroups"][ng]["name"]
        else:
            name = args.name

        if args.lifecycle == None:
            if cfg["managedNodeGroups"][ng]["spot"]:
                capacity_type = 'SPOT'
                lifecycle = 'Ec2Spot'
            else:
                lifecycle = 'OnDemand'
                capacity_type = 'ON_DEMAND'
        else:
            if args.lifecycle == 'spot':
                capacity_type = 'SPOT'
                lifecycle = 'Ec2Spot'
            else:
                lifecycle = 'OnDemand'
                capacity_type = 'ON_DEMAND'

        if args.list_subnets == []:
            list_subnets = []
            for sub in cfg["managedNodeGroups"][ng]["subnets"]:
                list_subnets.append(cfg["vpc"]["subnets"][re.sub("-.*$", "", sub)][sub]["id"])
        else:
            list_subnets = args.list_subnets

        if args.list_instance_types == []:
            list_instance_types = cfg["managedNodeGroups"][ng]["instanceTypes"]
        else:
            list_instance_types = args.list_instance_types

        if args.launch_template == None:
            launch_template = cfg["managedNodeGroups"][ng]["launchTemplate"]["id"]
        else:
            launch_template = args.launch_template

        if args.min_size == None:
            min_size = cfg["managedNodeGroups"][ng]["minSize"]
        else:
            min_size = args.min_size

        if args.max_size == None:
            max_size = cfg["managedNodeGroups"][ng]["maxSize"]
        else:
            max_size = args.max_size

        if args.desired == None:
            desired = cfg["managedNodeGroups"][ng]["desiredCapacity"]
        else:
            desired = args.desired

        if args.labels == None:
            labels = cfg["managedNodeGroups"][ng]["labels"]
        else:
            labels = args.labels[0]

        if args.node_role == None:
            node_role = cfg["managedNodeGroups"][ng]["iam"]["instanceRoleARN"]
        else:
            node_role = args.node_role

        if args.ami_type == None:
            ami_type = cfg["managedNodeGroups"][ng]["ami"]["amiType"]
        else:
            ami_type = args.ami_type

        print("Cluster name: ", cluster)
        print("Node group name: ", name)
        print("List of subnets: ", list_subnets)
        print("List of instance types: ", list_instance_types)
        print("Launch template id: ", launch_template)
        print("Lifecycle: ", lifecycle, " capacity_type: ", capacity_type)
        print("Min size: ", min_size, "   Max size: ", max_size, "   Desired size: ", desired)
        print("Kubernetes labels: ", labels)
        print("AMI type: ", ami_type)

        if name in list_ng:
            print("Node Group exists, will be updated")
            confirm = input(" CONFIRM EXECUTION? (yes / No): ")
            if confirm == 'yes':
                update_ng()
            else:
                print("NEXT")
                continue
        else:
            print("Node Group does not exists, will be created")
            confirm = input(" CONFIRM EXECUTION? (yes / No): ")
            if confirm == 'yes':
                create_ng()
            else:
                print("NEXT")
                continue
    print("EXIT")
    exit()

