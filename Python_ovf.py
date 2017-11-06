import requests
import click


def get_most_vote_answer_id(question_id):
    answer_api = 'https://api.stackexchange.com/2.2/questions/{}/answers?' \
                 'pagesize=1&order=desc&sort=votes&site=stackoverflow&' \
                 'filter=!*Jxb9s5EMYT2)PU5'.format(question_id)

    resp = requests.get(answer_api)
    answer_id = resp.json()['items'][0]['answer_id']

    return answer_id


def get_questions_data(page, tag):

    questions_api = 'https://api.stackexchange.com/2.2/questions?page={}&' \
                    'pagesize=10&order=desc&sort=votes&tagged={}&' \
                    'site=stackoverflow&filter=!-MOiNm40F1YI3cm' \
                    'Y125W3y40Bh*CGpQtD'.format(page, tag)

    resp = requests.get(questions_api)
    data = resp.json()

    return data


@click.command()
@click.argument('number', type=int)
@click.argument('tag')
def solve(number, tag):
    ''' This script return number the most vote question and answer of tag '''
    page = 1
    count = 0
    result = []

    try:
        while count < number:
            questions_data = get_questions_data(page, tag)

            if not questions_data['items']:
                number = 0
                break
            for item in questions_data['items']:
                title = item['title']
                link = item['link']
                question_id = item['question_id']

                most_vote_answer_id = get_most_vote_answer_id(question_id)
                most_vote_answer_link = '{0}{1}#{1}'.format(
                                        link, most_vote_answer_id)

                result.append('{}\n{}'.format(title, most_vote_answer_link))

                count += 1
                if count == number:
                    break
            page += 1
    except KeyError:
        click.echo(get_questions_data(page, tag)['error_message'])
    else:
        if not result:
            click.echo('Can\'t get any result')
    finally:
        click.echo('\n\n'.join(result))


def main():
    solve()


if __name__ == '__main__':
    main()
