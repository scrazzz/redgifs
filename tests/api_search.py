from redgifs import API, Tags, Order

import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        ret   = func(*args, **kwargs)
        end   = time.monotonic()
        print(f'\n{func.__name__} took {end - start}')
    return wrapper

@timer
def test_search(with_tags=False):
    api = API()
    
    if with_tags:
        result1 = api.search(Tags.milf)
        #print(result1)
        print('with_tags')
        return
    
    result2 = api.search('boobs')
    #print(result2)

@timer
def test_search2(with_tags=False):
    api = API()
    if with_tags:
        result3 = api.search(Tags.japanese, order=Order.top28)
        #print(result3)
        print('with_tags')
        return
   
    result4 = api.search('mia khalifa', order=Order.best)
    #print(result4)

if __name__ == '__main__':
    #test_search(True)
    test_search2(True)
