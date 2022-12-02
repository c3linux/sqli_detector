def extractParameters(url):
    extract_parameters = url[url.index("?")+1:]
    parameters = extract_parameters.split("&")
    return parameters

def extractPath(url):
    extract_parameters = url[:url.index("?")]
    return  extract_parameters