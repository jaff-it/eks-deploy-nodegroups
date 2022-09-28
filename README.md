# Script deploy-ng.py

The script is designed to deploy NodeGroups to EKS cluster. 
Since eksctl does not allow you to specify Launch Template and
Instance Types for a NodeGroups in one config.

The script takes one or more arguments:

Flag | Detail
--------------------------------------------------------------------------
-h, --help | show this help message and exit
--config-file CONFIG_FILE | set configuration file
--cluster CLUSTER | cluster name
-n NAME, --name NAME | node group name
-l LIFECYCLE, --lifecycle LIFECYCLE | Spot or on-demand
-s LIST_SUBNETS [LIST_SUBNETS ...], --list-subnets LIST_SUBNETS [LIST_SUBNETS ...] | List of subnets (--list-subnets subnet-id-1 subnet-id-2)
-t LIST_INSTANCE_TYPES [LIST_INSTANCE_TYPES ...], --list-instance-types LIST_INSTANCE_TYPES [LIST_INSTANCE_TYPES ...] | List of instance types (--list-instance-types r5.xlarge r5a.xlarge)
-L LAUNCH_TEMPLATE, --launch-template LAUNCH_TEMPLATE  | Launch template id
--min MIN_SIZE        Min size, default = 0
--max MAX_SIZE        Max size
--desired DESIRED     Desired size
--labels LABELS [LABELS ...] | Labels (--labels "'environment': 'develop', 'proj': 'my-project'")

