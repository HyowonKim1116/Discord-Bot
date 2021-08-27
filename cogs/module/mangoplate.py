#식당명 추출 함수
def getTitle(data):
    
    target = data.h2
    name = target.contents[0].replace('\n', '')

    while name[-1] == ' ':
        name = name[:-1]
    
    try:
        location = target.span.text
        return f'{name} {location}'
    except:
        return name

#식당 정보 추출 함수
def getInfo(data):

    rating = data.select_one('strong.search_point').text
    if rating == '': rating = 'None'

    category = data.select_one('p.etc').text
    view = data.select_one('span.view_count').text
    review = data.select_one('span.review_count').text
    link = 'https://www.mangoplate.com' + data.select_one('a').get('href')
    photo = data.select_one('img').get('data-original')

    return category, rating, view, review, link, photo