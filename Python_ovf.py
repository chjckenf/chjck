import sys

import requests


def get_most_vote_answer_id(question_id):
    answer_api = 'https://api.stackexchange.com/2.2/questions/{}/answers?' \
                 'pagesize=1&order=desc&sort=votes&site=stackoverflow&' \
                 'filter=!*Jxb9s5EMYT2)PU5'.format(question_id)

    resp = requests.get(answer_api)
    answer_id = resp.json()['items'][0]['answer_id']

    return answer_id


def get_questions_data(page, page_size, tag):

    questions_api = 'https://api.stackexchange.com/2.2/questions?page={}&' \
                    'pagesize={}&order=desc&sort=votes&tagged={}&' \
                    'site=stackoverflow&filter=!-MOiNm40F1YI3cm' \
                    'Y125W3y40Bh*CGpQtD'.format(page, page_size, tag)

    resp = requests.get(questions_api)
    data = resp.json()

    return data


def solve(input_data):

    if len(input_data) != 3:
        return 'Must take 2 argument'
    else:
        try:
            N = int(input_data[1])
        except ValueError:
            return 'Number of questions want to get must be integer'

    tag = input_data[2]

    page = 1
    page_size = 50
    count = 0

    result = []

    while count < N:
        questions_data = get_questions_data(page, page_size, tag)

        for item in questions_data['items']:
            title = item['title']
            link = item['link']
            question_id = item['question_id']

            ''' mva == Most vote answer '''
            mva_id = get_most_vote_answer_id(question_id)
            mva_link = '{0}{1}#{1}'.format(link, mva_id)

            result.append('{}\n{}'.format(title, mva_link))

            count += 1
            if count == N:
                break
        page += 1

    return '\n\n'.join(result)


def main():

    input_data = sys.argv
    result = solve(input_data)

    print(result)


if __name__ == '__main__':
    main()
