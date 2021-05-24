import requests
from argparse import RawTextHelpFormatter
import json
import sys
import shutil
import os
import argparse


class VKApi:
    def __init__(self, app_id=None, access_token=None, scope="photos", timeout=1):
        super().__init__()
        self.app_id = app_id

        self.uid = None

        self.scope = scope
        self.default_timeout = timeout

        # self.get_access_token()

        self.access_token = access_token

        self.session = requests.Session()


    @staticmethod
    def get_target_id():
        while True:
            print("Input id of the person, which album you want get (Also it may be your own id)")
            target_id = str(input())
            for i in target_id:
                if i not in [str(x) for x in range(10)]:
                    continue
            return target_id


    @staticmethod
    def download_photos(photos, album_id):
        cur_directory = os.path.dirname(os.path.abspath(__file__))
        dir_name = cur_directory + "/" + album_id
        postfix = 1
        while True:
            if os.path.isdir(dir_name):
                dir_name += "({0})".format(postfix)
            else:
                break
        os.mkdir(dir_name)
        urls = []
        # print(photos)
        for photo in photos:
            # максимальный размер находится в конце списка размеров фото
            file_url = photo["sizes"][-1]["url"]
            # print(file_url)
            urls.append(file_url)
        print("{count} photos to download".format(count=len(urls)))
        number = 1
        # print(urls)
        for url in urls:
            ext = "." + str(url.split(".")[-1])
            response = requests.get(url, stream=True)
            filename = dir_name + "/" + str(number) + ext
            with open(filename, "wb") as out:
                shutil.copyfileobj(response.raw, out)
            print("{number} downloaded...".format(number=number))
            number += 1
            del response
        print("check folder : {dir}".format(dir=dir_name))


    def get_photos(self):
        target_id = self.get_target_id()
        url = "https://api.vk.com/method/photos.getAlbums?owner_id={tid}&v=5.130&access_token={atoken}".format(
            tid=target_id, atoken=self.access_token)
        result = json.loads(requests.get(url).text)
        # print(result)
        albums = []
        if 'response' in result:
            count = result['response']['count']
            if count > 0:
                print("User with id={tid} has {count} albums:".format(tid=target_id, count=count))
            else:
                print("This user doesn't have public albums")
            for i in range(result['response']['count']):
                cur = result['response']['items'][i]['id']
                albums.append(cur)
                print(cur)
        print("Which one you want to see?")
        while True:
            album_id = int(input())
            if album_id in albums:
                url = "https://api.vk.com/method/photos.get?owner_id={oid}&album_id={aid}&v=5.130&access_token={atoken}".format(
                    oid=target_id, aid=album_id, atoken=self.access_token)
                result = json.loads(requests.get(url).text)
                result = result['response']
                count = result['count']
                photos = []
                for i in range(count):
                    photos.append(result['items'][i])
                    # print(photos)
                self.download_photos(photos, str(album_id))
                return
            else:
                print("No such album, try again.")


def main():
    print("Input your access token")
    access_token = str(input())
    print("Input app_id of your Standalone-application")
    app_id = str(input())
    api = VKApi(app_id=app_id, access_token=access_token)
    api.get_photos()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VK user albums photos getter\n\r------------------------\n"
                                                 "\n- Перед запуском Вам необходимо создать\n"
                                                 "\n- Standelone-приложение  Вконтакте\n\t"
                                                 "\n- Затем получить access token, "
                                                 "авторизовав пользователя с параметром scope=photos\n"
                                                 "\n\tподробнее см https://vk.com/dev/first_guide\n"
                                                 "\n- раздел Авторизация пользователя\n"
                                                 "\n- Откройте новую вкладку в браузере "
                                                 "и введите в адресную строку такой запрос:\n"
                                                 "\n- https://oauth.vk.com/authorize?client_id=5490057&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=photos&response_type=token&v=5.130\n"
                                                 "\n- Число 5490057 в запросе нужно заменить на API_ID вашего приложения.\n"
                                                 "\n- Нажмите Enter. Откроется окно с запросом прав. \n"
                                                 "\n- В нем отображаются название приложения, "
                                                 "иконки прав доступа, и ваши имя с фамилией. \n"
                                                 "\n- Нажмите «Разрешить». Вы попадете на новую страницу с предупреждением о том, "
                                                 "что токен нельзя копировать и передавать третьим лицам. \n"
                                                 "\nВ адресной строке будет URL "
                                                 "\thttps://oauth.vk.com/blank.html, а после # вы увидите дополнительные параметры — access_token, expires_in и user_id. \n"
                                                 "\nТокен может выглядеть, например, так: "
                                                 "\t51eff86578a3bbbcb5c7043a122a69fd04dca057ac821dd7afd7c2d8e35b60172d45a26599c08034cc40a\n",
                                     formatter_class=RawTextHelpFormatter)
    args = parser.parse_args()
    try:
        main()
    except KeyboardInterrupt:
        print("\nЗавершение работы скрипта")
        sys.exit(0)
