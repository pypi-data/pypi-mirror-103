#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: thepoy
# @Email: thepoy@163.com
# @File Name: jianshu.py
# @Created: 2021-04-07 09:00:26
# @Modified: 2021-04-28 10:49:23

import sys
import os
import json
import asyncio

import requests

from typing import Union, List, Optional, Tuple

from requests import Response

from mbs.blogs import logger
from mbs.utils.structs import BaseStruct
from mbs.utils.structs.jianshu import Category, NewCategory, Created, Updated, Published, Deleted, Error, OVER_FLOW
from mbs.utils.exceptions import ConfigFileNotFoundError
from mbs.utils.settings import CONFIG_FILE_PATH

Categories = List[Category]


def parse_response(struct: BaseStruct, resp: Response) -> BaseStruct:
    """解析响应

    Args:
        struct (BaseStruct): 响应对应的结构体
        resp (Response): 响应

    Returns:
        BaseStruct: 解析过的结构体
    """
    if resp.status_code == 200:
        return struct(resp.json())
    else:
        error = Error(resp.json())
        # TODO: 出错后，如果当前是在发布文章，则将当前文章进行标记，保存到数据库，
        # 之后再运行程序时，跳过之前被标记的发布出错的文章，以免草稿中出现太多重复文章
        if error.error[0]["code"] == OVER_FLOW:
            # TODO: 当天发布文章超过 2 篇，手动定时到明天发布。简书的定时发送是会员功能。
            pass
        logger.fatal(error.error)
        sys.exit(1)


class Jianshu:
    """简书 api"""
    headers = {
        "Accept":
        'application/json',
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0',
    }

    def __init__(self, cookies: Optional[dict] = None):
        if not cookies:
            self.__read_config_from_file()
        else:
            self.cookies = cookies
            self.__save_config_to_local_file()

    def __read_config_from_file(self):
        try:
            with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
                self.cookies = json.loads(f.read())["jianshu"]["cookies"]
        except FileNotFoundError:
            raise ConfigFileNotFoundError(
                "config file is not found, you should input the cookies of jianshu to create config file."
            )

    def __save_config_to_local_file(self):
        try:
            with open(CONFIG_FILE_PATH, "r+") as f:
                all_config = json.loads(f.read())
                all_config.update({"jianshu": {"cookies": self.cookies}})
                f.seek(0, 0)
                f.write(json.dumps(all_config))
                f.truncate()
        except FileNotFoundError:
            with open(CONFIG_FILE_PATH, "w") as f:
                f.write(json.dumps({"jianshu": {"cookies": self.cookies}}))

    def __get(self, url: str, headers: Optional[dict] = None) -> Response:
        if not headers:
            headers = self.headers
        return requests.get(url, headers=headers, cookies=self.cookies)

    def __post(self,
               url: str,
               data: Optional[dict] = None,
               headers: Optional[dict] = None) -> Response:
        if not headers:
            headers = self.headers
        if data:
            return requests.post(url,
                                 headers=headers,
                                 cookies=self.cookies,
                                 json=data)
        else:
            return requests.post(url, headers=headers, cookies=self.cookies)

    def __put(self,
              url: str,
              data: Optional[dict],
              headers: Optional[dict] = None) -> Response:
        if not headers:
            headers = self.headers

        return requests.put(url,
                            headers=headers,
                            cookies=self.cookies,
                            json=data)

    def get_categories(self) -> Optional[Categories]:
        url = "https://www.jianshu.com/author/notebooks"
        resp = self.__get(url)
        if resp.status_code == 200:
            categories = []
            for i in resp.json():
                categories.append(
                    Category({
                        "id": i["id"],
                        "name": i["name"],
                    }))
            return categories
        return None

    def __create_new_post(self, notebook_id: Union[str, int],
                          title: str) -> Optional[dict]:
        url = "https://www.jianshu.com/author/notes"

        data = {
            "notebook_id": str(notebook_id),
            "title": title,
            "at_bottom": False,
        }
        resp = self.__post(url, data)
        return parse_response(Created, resp)

    def __put_post(self,
                   postid: int,
                   title: str,
                   content: str,
                   version: int = 1):
        url = "https://www.jianshu.com/author/notes/%d" % postid

        # 将 content 中所有的图片上传到简书，用简书反回的图片链接进行替换
        content = asyncio.get_event_loop().run_until_complete(
            self._replace_all_images(content))

        data = {
            "id": str(postid),
            "autosave_control": version,
            "title": title,
            "content": content
        }

        resp = self.__put(url, data)
        return parse_response(Updated, resp)

    def __put_new_post(self, postid: int, title: str, content: str):
        return self.__put_post(postid, title, content)

    def __publish_new_post(self, postid: int):
        url = f"https://www.jianshu.com/author/notes/{postid}/publicize"
        data = {}

        resp = self.__post(url, data)
        return parse_response(Published, resp)

    def get_post(self, postid: Union[str, int]) -> str:
        url = f"https://www.jianshu.com/author/notes/{postid}/content"
        return self.__get(url).json()["content"]

    def new_post(self, notebook_id: Union[str, int], title: str,
                 content: str) -> str:
        created = self.__create_new_post(notebook_id, title)

        self.__put_new_post(created["id"], title, content)

        self.__publish_new_post(created["id"])

        return str(created.id)

    def delete_post(self, postid: Union[str, int]) -> Optional[dict]:
        url = f"https://www.jianshu.com/author/notes/{postid}/soft_destroy"

        resp = self.__post(url)
        return parse_response(Deleted, resp)

    def update_post(self, postid: Union[str, int], content: str):
        title, version, notebook_id = self._get_info_of_post(postid)
        put_result = self.__put_post(postid, title, content, version + 1)
        if put_result["content_size_status"] != "fine":
            logger.error(f"文章更新失败：{put_result}")
            sys.exit(1)

        self.__publish_new_post(postid)

    def _get_info_of_post(self, postid: int) -> Tuple[str, int, int]:
        notebook_id = self.__select_category_for_post(postid)
        url = f"https://www.jianshu.com/author/notebooks/{notebook_id}/notes"
        resp = self.__get(url)
        for note in resp.json():
            if note["id"] == postid:
                return note["title"], note["autosave_control"], notebook_id
        logger.error(f"没有找到 postid={postid} 的文章")
        sys.exit(1)

    def __select_category_for_post(self, postid: int):
        from mbs.utils.database import DataBase
        db = DataBase()
        sql = "SELECT c.jianshu_id FROM categories as c WHERE c.id = (SELECT p.category_id FROM posts p WHERE p.jianshu_id = %d)" % postid
        row = db.execute(sql).fetchone()
        if not row:
            return 0
        return row[0]

    def new_category(self, category: str) -> int:
        url = "https://www.jianshu.com/author/notebooks"
        data = {"name": category}

        resp = self.__post(url, data)
        if resp.status_code == 200:
            result = NewCategory(resp.json())
            return result.id
        else:
            error = Error(resp.json())
            logger.fatal(f"简书添加新分类出错：{error.error}")
            sys.exit(1)

    def update_category(self, category_id: Union[str, int],
                        category: str) -> bool:
        url = f"https://www.jianshu.com/author/notebooks/{category_id}"
        data = {"name": category}

        resp = self.__put(url, data)
        return resp.status_code == 204

    def delete_category(self, category_id: Union[str, int]) -> int:
        url = f"https://www.jianshu.com/author/notebooks/{category_id}/soft_destroy"
        return self.__post(url).status_code

    async def _replace_all_images(self, content: str) -> str:
        import re

        imgs = re.findall(r"!\[.+?\]\((.+?)\)", content)

        imgs = list(set(imgs))

        tasks = [self.upload_image(img) for img in imgs]

        logger.info("正在向简书上传文档内的图片...")
        new_imgs = await asyncio.gather(*tasks, return_exceptions=True)
        logger.info("已上传所有图片")

        new_imgs = set(new_imgs)
        for img in imgs:
            for new_img in new_imgs:
                if new_img[0] == img:
                    content = content.replace(
                        img, new_img[1] +
                        "imageMogr2/auto-orient/strip%7CimageView2/2/w/1240")
                    new_imgs.remove(new_img)
                    break

        return content

    def __get_token_and_key_of_local_image(self,
                                           filename: str) -> Tuple[str, str]:
        url = f"https://www.jianshu.com/upload_images/token.json?filename={filename}"
        headers = self.headers.copy()
        headers[
            "Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        resp = self.__get(url, headers=headers)
        return resp.json()["token"], resp.json()["key"]

    async def upload_image(self, path_or_url: str) -> Tuple[str, str]:
        if path_or_url.startswith("http"):
            url = "https://www.jianshu.com/upload_images/fetch"
            resp = self.__post(url, data={"url": path_or_url})
        else:
            if not os.path.exists(path_or_url):
                raise FileNotFoundError(f"没有找到 {path_or_url}")

            filename = os.path.basename(path_or_url).replace(" ", "_")

            token, key = self.__get_token_and_key_of_local_image(filename)

            # 根据 token 和 key 上传图片
            url = "https://upload.qiniup.com/"
            params = {
                "token": (None, token),
                "key": (None, key),
                "file": (filename, open(path_or_url, "rb")),
                "x:protocol": "https"
            }
            resp = requests.post(url, files=params)
        try:
            if "url" in resp.json():
                logger.debug("图片上传成功，本地或远程地址：%s，上传到简书后返回的地址：%self",
                             path_or_url,
                             resp.json()["url"])
            return (path_or_url, resp.json()["url"])
        except KeyError:
            logger.fatal(
                "上传图片时出错：%s",
                ", ".join([e["message"] for e in resp.json()["error"]]))
            sys.exit(1)

    def __str__(self):
        return "简书"


if __name__ == '__main__':
    j = Jianshu({
        "__yadk_uid":
        "hllzLGE562lyyUOwMIWkTUJGnCe6UDfR",
        "_ga":
        "GA1.2.1451964870.1617355260",
        "web_login_version":
        "MTYxNzM1ODY0MA%3D%3D--94bbfaeab24337a966b014f61b637decb2af0914",
        "Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068":
        "1617358494,1617366327,1617370546,1617372601",
        "remember_user_token":
        "W1s4Njg3MjU2XSwiJDJhJDExJGN3dllOSy41ck5mR0lNSGFRT1lxSi4iLCIxNjE4MjkyNjI5LjYwMjA0OTgiXQ%3D%3D--36c50928df3bf430883927844163f074c40c52ed",
        "read_mode":
        "day",
        "default_font":
        "font2",
        "locale":
        "zh-CN",
        "_m7e_session_core":
        "3d08cfa413d0fe3e16fb9df12f9c2ddc",
        "sensorsdata2015jssdkcross":
        "%7B%22distinct_id%22%3A%228687256%22%2C%22first_id%22%3A%2217891e2607f926-0f42742f0979a3-196c1a1f-3686400-17891e26080dba%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22desktop%22%2C%22%24latest_utm_medium%22%3A%22search-recent%22%7D%2C%22%24device_id%22%3A%2217891e2607f926-0f42742f0979a3-196c1a1f-3686400-17891e26080dba%22%7D"
    })

    # asyncio.run(
    # j.upload_image("/Users/thepoy/Desktop/截屏2021-04-25 21.54.28.png"))

    with open("/Volumes/MAC专用/markdown/Go/Golang 分布式系统.md",
              encoding="utf-8") as f:
        content = asyncio.get_event_loop().run_until_complete(
            j._replace_all_images(f.read()))
        print(content)
