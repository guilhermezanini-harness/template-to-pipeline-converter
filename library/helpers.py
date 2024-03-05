from urllib.parse import urlparse, parse_qs

def extract_parameters_from_url(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    query = parse_qs(parsed_url.query)
    return {
        "account_identifier": path_parts[path_parts.index('account') + 1],
        "org_identifier": path_parts[path_parts.index('orgs') + 1],
        "project_identifier": path_parts[path_parts.index('projects') + 1],
        "pipeline_identifier": path_parts[path_parts.index('pipelines') + 1],
    }

def merge(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge(value, node)
        else:
            destination[key] = value

    return destination

def find_paths_with_input_value(json_object, path=""):
    """
    Recursive function to identify which attributes have a "<+input>" value
    and return an array with all JSON paths that includes this "<+input>".
    """
    paths_with_input = []

    if isinstance(json_object, dict):
        for key, value in json_object.items():
            new_path = f"{path}.{key}" if path else key  # Construct the new path
            paths_with_input.extend(find_paths_with_input_value(value, new_path))
    elif isinstance(json_object, list):
        for index, item in enumerate(json_object):
            new_path = f"{path}[{index}]"
            paths_with_input.extend(find_paths_with_input_value(item, new_path))
    elif json_object == "<+input>":
        paths_with_input.append(path)

    return paths_with_input

def update_json_values(original_json, paths, values_json):
    """
    Updates the values in the original JSON object based on the provided paths
    and corresponding values from another JSON structure.
    
    :param original_json: The original JSON object to update.
    :param paths: List of paths indicating where to update the values.
    :param values_json: JSON object containing the new values.
    """
    def set_value_by_path(obj, path, new_value):
        """
        Sets a value in a nested JSON object based on a dot-separated path.
        
        :param obj: The JSON object to update.
        :param path: The path where to set the value.
        :param new_value: The new value to set.
        """
        parts = path.split('.')
        for part in parts[:-1]:  # Navigate through the path until the last key
            if '[' in part:  # If the part is a list index
                idx = int(part[part.find('[')+1:part.find(']')])
                part = part[:part.find('[')]
                obj = obj[part][idx]
            else:  # If the part is a dictionary key
                obj = obj[part]
        last_part = parts[-1]
        if '[' in last_part:  # Set the value in a list
            idx = int(last_part[last_part.find('[')+1:last_part.find(']')])
            last_part = last_part[:last_part.find('[')]
            obj[last_part][idx]['value'] = new_value
        else:  # Set the value in a dictionary
            obj[last_part] = new_value

    # Extract the templateInputs directly since we know the structure is consistent for what we need
    template_inputs = values_json['pipeline']['template']['templateInputs']

    # Update the original JSON sample using the paths and corresponding values
    for path in paths:
        # Since paths include 'template.spec', which isn't in the template_inputs, adjust the path
        adjusted_path = path.replace('template.spec.', '')
        # Split the path to find the corresponding value in template_inputs
        value_path_parts = adjusted_path.split('.')
        current_value_obj = template_inputs
        for part in value_path_parts:
            if '[' in part and ']' in part:  # Handle list indices
                idx = int(part[part.find('[')+1:part.find(']')])
                part = part[:part.find('[')]
                current_value_obj = current_value_obj[part][idx]
            elif part != 'value':  # Navigate through dictionaries
                current_value_obj = current_value_obj.get(part, {})
            else:
                break  # Once we reach 'value', we stop since we're at the target

        # Now, current_value_obj should contain the 'value' field with the new value
        new_value = current_value_obj['value'] if 'value' in current_value_obj else None
        if new_value:
            set_value_by_path(original_json, path, new_value)
    return original_json

def find_and_update_json_values(json_obj, values_json):
    """
    Finds all attributes with "<+input>" in the JSON object and updates them with corresponding
    values from another JSON structure.
    
    :param json_obj: The original JSON object to search and update.
    :param values_json: JSON object containing the new values.
    """
    paths = find_paths_with_input_value(json_obj)
    return update_json_values(json_obj, paths, values_json)