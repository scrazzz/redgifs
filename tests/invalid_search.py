from redgifs import API

def test_invalid():
    api = API()
    result = api.search('abcd')
    print(result)

if __name__ == '__main__':
    test_invalid()
