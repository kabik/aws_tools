import re
import urllib.request

TOP_URL = 'https://docs.aws.amazon.com/cli/latest/reference/'

top_req = urllib.request.Request(TOP_URL)
with urllib.request.urlopen(top_req) as top_res:
    top_body = top_res.read().decode()
    ref_list = re.findall(r'(?<=<a class=\"reference internal" href=\")[^#\.].*(?=index.html\">)', top_body)

    url_list = []
    for ref in ref_list:
        url = TOP_URL + ref
        print(url)
        req_1 = urllib.request.Request(url)
        with urllib.request.urlopen(req_1) as res:
            body_1 = res.read().decode()
            sg = re.findall(r'security-group', body_1)
            if len(sg):
                print('    exists')
                url_list.append(url)

    print('=== RESULT ===')
    for url in url_list:
        print(url)
