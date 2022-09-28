# Script deploy-ng.py

The script is designed to deploy NodeGroups to EKS cluster. 
Since eksctl does not allow you to specify Launch Template and
Instance Types for a NodeGroups in one config.

**Prerequires:**

Script uses modules boto3 pyyaml argparse

`pip install boto3 pyyaml argparse`

_You can also use Docker_

## Docker

Copy Dockerfile and run the command :

`docker build -t node-groups .`

To use the container, run the command :

```
docker run -it --rm \
    --env AWS_DEFAULT_PROFILE \
    --env AWS_ACCESS_KEY_ID \
    --env AWS_SECRET_ACCESS_KEY \
    -v ~/.aws:/root/.aws \
    -v $(pwd):/app \
    node-groups:latest bash
```
or
````
docker run -it --rm \
    --env AWS_DEFAULT_PROFILE=<my-aws-profile> \
    --env AWS_ACCESS_KEY_ID=<xxxxxxxxxxxxxxx> \
    --env AWS_SECRET_ACCESS_KEY=<XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX> \
    -v ~/.aws:/root/.aws \
    -v $(pwd):/app \
    node-groups:latest bash
````

Config file and script must be in the current directory when starting the container, or replace

`-v $(pwd):/app`

to 

`-v <path/to/script/dir>:/app`

In container run 

`python ./deploy-ng.py [PARAMETERS]`


The script takes one or more arguments:

Flag | Detail
-----|--------------------------------------------------------------------
-h, --help | show this help message
--config-file CONFIG_FILE | set configuration file
--cluster CLUSTER | cluster name
-n NAME, --name NAME | node group name
-l LIFECYCLE, --lifecycle LIFECYCLE | Spot or on-demand
-s LIST_SUBNETS [LIST_SUBNETS ...], --list-subnets LIST_SUBNETS [LIST_SUBNETS ...] | List of subnets (--list-subnets subnet-id-1 subnet-id-2)
-t LIST_INSTANCE_TYPES [LIST_INSTANCE_TYPES ...], --list-instance-types LIST_INSTANCE_TYPES [LIST_INSTANCE_TYPES ...] | List of instance types (--list-instance-types r5.xlarge r5a.xlarge)
-L LAUNCH_TEMPLATE, --launch-template LAUNCH_TEMPLATE  | Launch template id
--min MIN_SIZE    |    Min size, default = 0
--max MAX_SIZE    |   Max size
--desired DESIRED  |   Desired size
--labels LABELS [LABELS ...] | Labels (--labels "'environment': 'develop', 'project': 'my-project'")


**If --config-file is used, then other cli arguments take precedence over the values in the config.**



