import re


def get_original_registrations(path_to_content_map, protocol_to_protocol_functions):
    files = list(path_to_content_map.values())
    result = {}
    for protocol in protocol_to_protocol_functions:
        for file in files:
            if "register(" + protocol in file:
                registration = re.findall(
                    r".*container.register\(" + protocol + r"[\s\S]+?}", file
                )[0].replace(protocol + ".self", protocol + "Impl.self")

                result[protocol] = registration
    return result
