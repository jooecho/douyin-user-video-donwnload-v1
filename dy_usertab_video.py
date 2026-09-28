from DrissionPage import ChromiumPage
import requests
import re
import os
import json



share_link = input("请输入分享链接")

#打开浏览器
browser=ChromiumPage()

browser.listen.start('aweme/post')
#访问网站
browser.get("https://www.douyin.com/user/MS4wLjABAAAAXrcPvX8QchAY5irWMAxU379DgfCBEOoztZoCcOUqi8I?from_tab_name=main&vid=7689399959444200313")
import os
os.makedirs('video', exist_ok=True)

page = 1
while True:
    try:
        print(f'正在采集{page}页的数据内容')
        
        resp = browser.listen.wait(timeout=5)

        if resp is False:         
            print('没有更多数据包，采集结束')
            break

        json_data = resp.response.body
        for index in json_data.get('aweme_list', []):
            video_id = index['aweme_id']
            title = index.get('desc') or index.get('item_title') or str(video_id)
            video_url = index['video']['play_addr']['url_list'][-1]
            print(video_id, title)

            if '.mp3' in video_url:
                continue

            new_title = re.sub(r'[\\/:*?"<>|\r\n]', '', title)
            filepath = os.path.join('video', new_title + '.mp4')

            video_content = requests.get(video_url, timeout=30).content
            with open(filepath, 'wb') as f:
                f.write(video_content)

        browser.scroll.to_bottom()   
        page += 1

    except Exception as e:
        print(f'发生错误: {e}')
        continue
        '''
        代码逻辑:
        代码通过browser.listen.start('aweme/post')监听数据包,预览拦截,后续所有请求路径包含aweme/post 都会被拦截
        再通过resp.response.body获取响应的json数据,然后遍历json数据中的aweme_list
        取每个aweme_list的video/play_addr/url_list[-1] 
        放到request.get里取请求
        然后保存到本地
        
        补充:
        browser.listen.wait是捕获即执行,一但捕捉到一个POST请求响应
        就会立即执行,如果多条POST请求,那么多条POST会进入队列,browser.listen.wait会从队列中取出一条来执行
        
        '''


