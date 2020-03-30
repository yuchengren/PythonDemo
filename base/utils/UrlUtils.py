

def parseUrlParam(url):
    if len(url) == 0:
        return {}
    param_str_list = url.split("?")
    if len(param_str_list) <= 1:
        return {}
    param_dict_list = param_str_list[1].split("&")
    _dict = {}
    for param_entry_str in param_dict_list:
        param_entry_list = param_entry_str.split("=")
        if len(param_str_list) <= 1:
            break
        _dict[param_entry_list[0]] = param_entry_list[1]
    return _dict


