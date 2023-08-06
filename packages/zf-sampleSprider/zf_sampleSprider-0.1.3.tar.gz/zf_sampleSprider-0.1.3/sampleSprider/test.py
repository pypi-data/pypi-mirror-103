
if __name__=='__main__':
    with open('D://SampleSprider/taobao_cookies.txt','r') as file:
        cookies=eval(file.read())
        print(type(cookies))
        print(cookies)