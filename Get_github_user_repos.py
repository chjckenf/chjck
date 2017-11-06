import requests
import click


def user_repos(input_data):
    result = []

    for data in input_data:
        result.append('Repo name: {}\t---\tHtml url: {}'.format(
            data['name'], data['html_url']))

    return '\n'.join(result)


@click.command()
@click.argument('user')
def solve(user):
    ''' This simple script return repos of user '''
    resp = requests.get('https://api.github.com/users'
                        '/{}/repos'.format(user))
    status_code = resp.status_code // 100

    if status_code == 4:
        return 'User not found. Please try again'
    elif status_code == 5:
        return 'Server is not ok. Please try again later'
    else:
        data = resp.json()
        click.echo(user_repos(data))


def main():
    solve()


if __name__ == '__main__':
    main()
