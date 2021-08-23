import discord
import requests
import urllib.parse
import json

#URL 추출 함수
def getUrl(keyword):

    encoded_search = urllib.parse.quote_plus(keyword)
    url = f'https://www.youtube.com/results?search_query={encoded_search}&sp=EgIQAQ%253D%253D'
    response = requests.get(url).text
    while 'ytInitialData' not in response:
        response = requests.get(url).text
    
    start = (
        response.index('ytInitialData')
        + len('ytInitialData')
        + 3
    )
    end = response.index('};', start) + 1
    
    json_str = response[start:end]
    data = json.loads(json_str)

    videos = data['contents']['twoColumnSearchResultsRenderer']['primaryContents'][
        'sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
        
    for row in videos:
        video_data = row.get('videoRenderer', {})
        return 'https://www.youtube.com/' + video_data.get('navigationEndpoint', {}).get('commandMetadata', {}).get('webCommandMetadata', {}).get('url', None)

#정보 임베드 함수
def getInfo(data):

    view_count = '{0:,}'.format(data['view_count'])
    average_rating = data['average_rating']

    try:
        like_count = '{0:,}'.format(data['like_count'])
    except:
        like_count = '비공개'
    
    embed = discord.Embed(
        title = data['title'],
        url = data['webpage_url'],
        color = discord.Color.red()
    )
    embed.add_field(name = '조회수', value = view_count, inline = True)
    embed.add_field(name = '평점', value = average_rating, inline = True)
    embed.add_field(name = '좋아요 수', value = like_count, inline = True)
    embed.set_author(name = data['uploader'], url = data['uploader_url'])
    embed.set_image(url = data['thumbnail'])

    return embed

#시간 변환 함수
def getTime(data):

    if data['duration'] == 0:
        duration = ' 실시간 스트리밍 중'
    
    else:
        duration = ''
        
        duration_hour = data['duration'] // 3600
        duration_min = (data['duration'] % 3600) // 60
        duration_sec = data['duration'] % 60
        
        duration_list = [
            [duration_hour, '시간'],
            [duration_min, '분'],
            [duration_sec, '초']
        ]
        
        for i in range(3):
            item = duration_list[i]
            if item[0]:
                duration += f' {item[0]}{item[1]}'
    
    return duration
