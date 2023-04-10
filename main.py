import requests
import os
import random

def text_between(s, l, r):
    ret = []
    beg = 0
    end = 0
    while 1:
        beg = s.find(l, end)
        if beg == -1:
            return ret
        else:
            end = s.find(r, beg)
        ret.append(s[beg:end+len(r)])

def del_between(s, l, r):
    beg = 0
    end = 0
    while 1:
        beg = s.find(l)
        if beg == -1:
            return s
        else:
            end = s.find(r)
        s = s[:beg] + s[end+len(r):]
            
def grab_from_url(url):

    go = 5
    while go:
        try:
            html = requests.get(url).text
            print(url)
            go = 0
        except Exception:
            go -= 1


    # extract title from html document
    try:
        title = del_between(text_between(html, '<title data-rh="true">', '</title>')[0], '<', '>')[:-5]
    except Exception:
        return

    if title not in ['你似乎来到了没有知识存在的荒原', '抱歉，该内容已被作者删除']:

        # extract answers from html document
        answers = text_between(html, '<span class="RichText ztext', '</span>')
        for i in range(0, len(answers)):
            answers[i] = del_between(answers[i], '<', '>')

        if len(answers) == 0:
            return

        # combine title and answers in the same list of strings
        output = [title] + answers

        # extract time from html document
        time = text_between(html, 'dateCreated', '/')[0][22:-7].replace(':', ' ').replace('.', ' ').replace('T', ' ').replace('-', ' ')
        

        # check if directory 'questions' exists, if not, create one
        if not os.path.exists('questions'):
            os.mkdir('questions')

        # write to a file in to the 'questions' directory
        filename = 'questions/' + url.split('/')[-1] + ' ' + time + '.txt'
        with open(filename, 'w', encoding='utf-8') as file:
            print('New File')
            for i in range(0, len(output)):
                file.write(output[i])
                if i != len(output)-1:
                    file.write('\n<dgut>\n')


# def next_url():
    
#     current = 19550225
#     step = 10000

#     if os.path.exists('current.txt'):
#         with open('current.txt', 'r') as file:
#             current = int(file.read())
    
#     grab_from_url('https://www.zhihu.com/question/' + str(current))

#     with open('current.txt', 'w') as file:
#         file.write(str(current + step + random.randint(0, 10)))

def next_url():

    start = 19550225
    end = 600000000
    current = random.uniform(0, 1)**2
    grab_from_url('https://www.zhihu.com/question/' + str(int(start + current*(end - start))))

while True:
    next_url()
