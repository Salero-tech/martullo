

def insertMsg (resp, key, replaceWith):
    if key in resp:
                resp = resp.replace(key, str(replaceWith))
    return resp