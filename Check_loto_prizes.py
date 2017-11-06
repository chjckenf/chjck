import requests
from bs4 import BeautifulSoup as BS
import click


def loto_prizes(data):
    loto_prizes = data.find(id="result_tab_mb").find(
                  'tbody').get_text(' ').split()

    prizes = [i for i in loto_prizes if i.isnumeric()]

    try :
        result = '''
    Đặc biệt:\t{}\n
    Giải nhất:\t{}\n
    Giải nhì:\t{}\t{}\n
    Giải ba:\t{}\t{}\t{}\t{}\t{}\t{}\n
    Giải tư:\t{}\t{}\t{}\t{}\n
    Giải năm:\t{}\t{}\t{}\t{}\t{}\t{}\n
    Giải sáu:\t{}\t{}\t{}\n
    Giải bảy:\t{}\t{}\t{}\t{}\n
    '''.format(*prizes)
    except IndexError:
        return 'Xo so van con dang quay'

    return result


def lotos(data, numbers):
    lotos = data.find(id="loto_mb").find('tbody').get_text(' ').split()

    result = []
    for number in numbers:
        if number in lotos:
            result.append('{} trung {} nhay'.format(number, lotos.count(number)))
        else:
            result.append('{} khong trung'.format(number))

    return '\n'.join(result)


@click.command()
@click.argument('numbers', nargs=-1)
def solve(numbers):
    ''' Kiem tra so nhap vao co trung lo hay khong. Neu khong nhap so nao, se tra ve tat ca cac giai '''
    resp = requests.get('http://ketqua.net/')
    data = BS(resp.text, 'lxml')

    if len(numbers) == 0:
        click.echo(loto_prizes(data))
    else:
        try:
            temp = [int(number) for number in numbers]
        except ValueError:
            click.echo('Chi nhan so')
        else:
            click.echo(lotos(data, numbers))


def main():
    solve()


if __name__ == '__main__':
    main()
