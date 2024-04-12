# Парсинг
# http://jsonplaceholder.typicode.com/

import requests
from collections import defaultdict


posts_url = "http://jsonplaceholder.typicode.com/posts"
comments_url = "http://jsonplaceholder.typicode.com/comments"


def main(posts_url, comments_url):
    # Получение данных
    posts_response = requests.get(posts_url)
    comments_response = requests.get(comments_url)

    posts_data = posts_response.json()
    """
    [{'userId': 1, 'id': 1, 'title': 'sunt aut',
     'body': 'eveniet architecto'}, ... ]
    """
    comments_data = comments_response.json()
    """
    [{'postId': 1, 'id': 1, 'name': 'et quam laborum',
     'email': 'Eliseo@gardner.biz',
      'body': 'laudant accusantium'}, ...]
    """

    # Агрегация данных
    count_post_comment = {}
    for c in comments_data:
        count_post_comment[c['postId']] = count_post_comment.get(c['postId'], 0) + 1

    count_user_comments = {}
    for p in posts_data:
        count_user_comments[p['userId']] = (count_user_comments.get(p['userId'], (0, 0))[0] + 1,
                                            count_user_comments.get(p['userId'], (0, 0))[1]
                                            + count_post_comment[p['id']])

    result = {k: v[1] / v[0] for k, v in count_user_comments.items()}
    print(result)


if __name__ == '__main__':
    main(posts_url, comments_url)

