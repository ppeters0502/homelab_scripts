import json
import yaml

def parse_containers(inspect_path):
    with open(inspect_path, 'r') as f:
        containers = json.load(f)

    result = []
    for container in containers:
        name = container.get('Name', '').lstrip('/')
        mounts = container.get('Mounts', [])
        data_dirs = []
        for mount in mounts:
            # Only include bind mounts and named volumes
            if mount.get('Type') in ['bind', 'volume']:
                source = mount.get('Source')
                if source:
                    data_dirs.append(source)
        if data_dirs:
            result.append({'name': name, 'data_dirs': data_dirs})

    return result

if __name__ == '__main__':
    containers_list = parse_containers('./docker_containers_inspect.json')
    print(yaml.dump({'containers': containers_list}, sort_keys=False, default_flow_style=False))