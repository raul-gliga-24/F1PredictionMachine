import json, re
data = open('full_response.txt', encoding='utf-16le').read()
match = re.search(r'`json\s*(.*?)\s*`', data, re.DOTALL)
s = match.group(1) if match else data
print('REGEX MATCH:', bool(match))
try:
    json.loads(s)
    print('JSON PARSED OK')
except Exception as e:
    print('JSON PARSE ERR:', e)
