import re
import urllib.parse
import urllib.request


async def geturl(query):
    query_string = urllib.parse.urlencode({"search_query": query})

    format_url = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)

    search_results = re.findall(r"watch\?v=(\S{11})", format_url.read().decode())

    return "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
