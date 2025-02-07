import os
import requests
import json

result_data = []
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "application/json"  # JSON 응답을 원한다고 명시
}
# 페이지들 로드
urls = ['https://e.kakao.com/api/v1/items/t/dyu-ganadi-2']  # 크롤링할 URL 리스트

# 저장할 폴더 이름 설정 (폴더가 없다면 생성)
save_folder = "kakao_emoticons"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

for url in urls:
    response = requests.get(url, headers=headers)

    data = response.json()
    
    # 제목
    title = data['result']['title']
    item_folder = os.path.join(save_folder, title.replace(" ", "_"))

    # 상품url(상품영어이름), 작가ID
    title_url = data['result']['titleUrl']
    artistID = data['result']['creator']['id']
    
    # 비슷한 스타일 similarStyleItems
    similarStyleItems = data['result']['similarStyleItems']
    
    #폴더가 이미 존재하면 건너뛰고 다음 URL로
    if os.path.exists(item_folder):
        continue
    
    os.makedirs(item_folder, exist_ok=True)
    
    # 이미지 URL 리스트
    thumbnail_urls = data["result"]["thumbnailUrls"]
    print(thumbnail_urls)


    for idx, img_url in enumerate(thumbnail_urls):
        file_name = os.path.join(item_folder, f"image_{title_url}_{idx+1}.jpg")
        print(f"Downloading {img_url} to {file_name}")

        try:
            # 이미지 다운로드
            img_data = requests.get(img_url,headers=headers).content
            with open(file_name, "wb") as f:
                f.write(img_data)
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")
            
    tag = data['result']['styleTags']
    print(tag)
    artist = data['result']['artist']
    print(artist)
    
    #JSON에 저장할 데이터 구성
    item_data = {
        "title": title,
        "title_url":title_url,
        "artist": artist,
        "artistID": artistID,
        "tag": tag,
        "similarStyleItems":similarStyleItems,
        "image_urls": thumbnail_urls
    }
    
    result_data.append(item_data)



# 크롤링한 데이터를 JSON 파일로 저장
with open(f"kakao_emoticons_data_{title_url}.json", "w", encoding="utf-8") as json_file:
    json.dump(result_data, json_file, ensure_ascii=False, indent=4)
        
