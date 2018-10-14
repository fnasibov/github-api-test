import json

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max, Min
from django.http import HttpResponse
from django.template.loader import get_template

from github.models import Issue


def show_issues(request):
    update_issues_data()
    template = get_template('index.html')
    (min_comments_count_issues, max_comments_count_issues, comments_count_greather_ten) = load_issue_lists()
    html = template.render({'title': 'WTF!?!',
                            'max_comment_issues': max_comments_count_issues,
                            'min_comment_issues': min_comments_count_issues,
                            'comments_count_greather_ten': comments_count_greather_ten})
    return HttpResponse(html)


def load_issue_lists():
    issues = Issue.objects.all()
    comments_count_extremum = issues.aggregate(Max('comments_count'), Min('comments_count'))
    min_comments_count_issues = []
    max_comments_count_issues = []
    comments_count_greather_ten = []
    for issue in issues:
        if issue.comments_count == comments_count_extremum['comments_count__max']:
            max_comments_count_issues.append(issue)
            continue
        if issue.comments_count >= 10:
            comments_count_greather_ten.append(issue)
            continue
        if issue.comments_count == comments_count_extremum['comments_count__min']:
            min_comments_count_issues.append(issue)
    return min_comments_count_issues, max_comments_count_issues, comments_count_greather_ten


def update_issues_data():
    response = requests.get('https://api.github.com/repos/django/channels/issues')
    if response.status_code == 200:
        decoded_issues = json.loads(response.content)
        for item in decoded_issues:
            comments = json.loads(requests.get(item['comments_url']).content)
            try:
                issue = Issue.objects.get(github_id=item['id'])
                issue.comments_count = len(comments)
                issue.title = item['title']
                issue.save()
            except ObjectDoesNotExist:
                issue = Issue(github_id=item['id'], url=item['html_url'], title=item['title'],
                              comments_count=len(comments))
                issue.save()
