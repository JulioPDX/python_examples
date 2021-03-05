import requests
from rich.console import Console
from rich.table import Table
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

c = Console()

base_url = "https://your-panorama.local/restapi/"
temp_stacks = "v10.0/Panorama/TemplateStacks"
device_group = "v10.0/Panorama/DeviceGroups"

template_url = base_url + temp_stacks
dg_url = base_url + device_group

headers = {
    "X-PAN-KEY": "somekey",
}

device_group_table = Table(title="Device Group Stats")
device_group_table.add_column("Group Name", justify="center", style="spring_green3")
device_group_table.add_column("Devices in Group", justify="center", style="purple")

get_dg = requests.get(dg_url, headers=headers, verify=False)

for group in get_dg.json()["result"]["entry"]:
    try:
        device_group_table.add_row(
            f"{group['@name']}", f"{len(group['devices']['entry'])}"
        )
    except KeyError:
        device_group_table.add_row(f"{group['@name']}", "0")

c.print(device_group_table)

stack_table = Table(title="Template Stack Stats")
stack_table.add_column("Template Stack Name", justify="center", style="spring_green3")
stack_table.add_column("Devices in Stack", justify="center", style="purple")

get_template = requests.get(template_url, headers=headers, verify=False)

for group in get_template.json()["result"]["entry"]:
    try:
        stack_table.add_row(
            f"{group['@name']}", f"{len(group['devices']['entry'])}"
        )
    except KeyError:
        stack_table.add_row(f"{group['@name']}", "0")

c.print(stack_table)
