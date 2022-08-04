import re, urllib.parse, urllib.request


async def geturl(content):
    music_name = content.strip('jedi yt ')

    query_string = urllib.parse.urlencode({"search_query": music_name})

    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)

    search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())

    return "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
