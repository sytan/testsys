import re, time

def timeout(timeout,start):
    eclapse = time.time() - start
    if eclapse >= timeout:
        isTimeout = True
    else:
        isTimeout = False
    return isTimeout

def toBool(string):
    string = string.capitalize()
    if string == 'True':
        return True
    else:
        return False

def toNone(string):
    string = string.capitalize()
    if string == 'None':
        string = None
    return string

def strExtract (string,splitLeft = "\[",splitRight = "\]"):
    try:
        reStr = re.escape(splitLeft)+"(.*)"+re.escape(splitRight)
        extract = re.findall(reStr, string)[0]
    except IndexError:
        extract = ""
        isExtract = False
        prefix = string
        suffix = ""
    else:
        isExtract = True
        split = string.split(splitLeft+extract+splitRight)
        prefix = split[0]
        suffix = split[1]
    return isExtract, prefix, extract, suffix

def endline(string):
    if string == "\n":
        return "\n"
    elif string == "\r":
        return "\r"
    elif string == "\r\n":
        return "\r\n"
    else:
        return ""
        
def formatData(msg, cmd=""):
    data = {"msg":msg, "cmd":cmd}
    return data

if __name__ == "__main__":

    string = "rfpi = ([0-9A-Za-f]{10})\[RFPI\]are you ok"
    print strExtract(string)
