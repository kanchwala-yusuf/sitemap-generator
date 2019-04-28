import yaml
import json

# As for the cleanup: because of the alternating lists and
# dicts it is a bit more complex, but the following works:
def walker(coll):
    if isinstance(coll, list):
        for item in coll:
            yield item
    if isinstance(coll, dict):
        for item in coll.values():
            yield item

def deleter(coll):
    for data in walker(coll):
        if data == [] or data == {}:
            coll.remove(data)
        deleter(data)


# Create sitemap from the given links
def create_sitemap(links):

    # Paths
    paths = []

    # Every link crawled
    for item in links:

        # strip the '/'
        item = item.strip('/')

        # split at '/'
        split = item.split('/')

        # discard ("https:/", '/') and append to paths
        paths.append(split[2:])

    # Loop over these paths, building the format as we go along
    root = {}
    for path in paths:
        branch = root.setdefault(path[0], [{}, []])
        for step in path[1:-1]:
            branch = branch[0].setdefault(step, [{}, []])
        branch[1].append(path[-1])

    deleter(root)

    # sitemap yaml
    sitemap_yaml = yaml.dump(root, default_flow_style=False, allow_unicode=True)
    print("sitemap YAML:\n%s" % sitemap_yaml)

    # sitemap json
    sitemap_json = json.dumps(root, sort_keys=True)

    return sitemap_json
