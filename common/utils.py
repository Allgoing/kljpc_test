# -- coding: utf-8 --


def str_to_dict(check_point):
    result = check_point.split(',')
    return result


if __name__ == '__main__':
    a = str_to_dict('code:200,message:success')
    print(a)


