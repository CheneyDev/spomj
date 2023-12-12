import requests
import time

# API 请求的 URL
submit_url = "https://api.abc.top/mj/submit/imagine"
fetch_url_template = "https://api.abc.top/mj/task/{}/fetch"

# 设置请求头部
headers = {
    "mj-api-secret": "sk-123",
    "Content-Type": "application/json",
}

# 设置请求体
data = {
    "base64Array": [],
    "botType": "MID_JOURNEY",
    "instanceId": "",
    "modes": [],
    "notifyHook": "",
    "prompt": "flying Cat",
    "remix": True,
    "remixAutoConsidered": True,
    "state": ""
}

# 发送 POST 请求
submit_response = requests.post(submit_url, json=data, headers=headers)

# 解析响应的 JSON 内容
submit_response_json = submit_response.json()

# 打印整个响应内容
print("提交响应:", submit_response_json)

# 获取 'result' 字段的值
result = submit_response_json.get('result', None)

if result:
    fetch_url = fetch_url_template.format(result)

    while True:
        # 发送 GET 请求
        fetch_response = requests.get(fetch_url, headers=headers)

        # 检查响应状态码
        if fetch_response.status_code != 200:
            print(f"请求失败，状态码：{fetch_response.status_code}")
            break

        # 检查响应体是否为空
        if not fetch_response.content:
            print("响应体为空")
            break

        try:
            fetch_response_json = fetch_response.json()
            # 检查任务状态
            status = fetch_response_json.get('status')
            progress = fetch_response_json.get('progress')
            if status == 'SUCCESS' and progress == '100%':
                image_url = fetch_response_json.get('imageUrl')
                if image_url:
                    print("任务执行成功!")
                    print("Image URL:", image_url)
                    break
                else:
                    print("未找到有效的 Image URL")
                    break
            else:
                print("当前进度:", progress)
                time.sleep(2)  # 等待 2 秒
        except requests.JSONDecodeError:
            print("响应不是有效的 JSON 格式")
            break
else:
    print("未找到result字段")