import json
from typing import Optional

import requests
from yuheng import logger
from yuheng.method.network import get_endpoint_api


def oauth_login():

    REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
    CLIENT_ID = "1lMl1Wdv8GRAGqtB9ptzaWqxdvWkee6Jsf6xwD8oeoE"
    CLIENT_SECRET = ""

    def get_oauth_login_page() -> str:
        url_login_page = (
            "{AUTHORIZE_URL}"
            + "?response_type=code"
            + "&client_id={CLIENT_ID}"
            + "&redirect_uri={REDIRECT_URI}"
            + "&scope={SCOPE}"
        )
        authorize_url = get_endpoint_api("osm-dev")[:-3] + "oauth2/authorize"
        client_id = CLIENT_ID
        redirect_uri = REDIRECT_URI
        scope = ["read_prefs", "write_api"]
        return (
            url_login_page.replace("{AUTHORIZE_URL}", authorize_url)
            .replace("{CLIENT_ID}", client_id)
            .replace("{REDIRECT_URI}", redirect_uri)
            .replace("{SCOPE}", "%20".join(scope))
        )

    def get_application_code(login_page: str, method="code") -> Optional[str]:
        """
        策略有两种，一个是code代表手动输入获取到的code，另一个是listen
        当设置为code的时候，如果检测到本地系统环境变量有，就用，否则就要求输入（初期直接强制输入吧）
        设置为listen的时候，就起一个本地的服务器来获取(这个能实现工具全自动化，只需要点一下授权，但是会很臃肿)
        要实现绝对的自动化还是得code模式读取本地

        不管怎样，打开页面都是难免的
        """

        import webbrowser

        webbrowser.open(login_page)

        if method.lower() == "listen":
            import fastapi
            import uvicorn

            code: str = ""
            logger.success(f"[get_application_code] GET FROM WEBHOOK: {code}")
        elif method.lower() == "code":

            # 这里可以尝试读取本地code了

            code: str = input("请输入在网页上获取到的code：")

            logger.success(
                f"[get_application_code] GET FROM CLIPBOARD: {code}"
            )
        else:
            logger.error("怎么搞的")
            return None

        return code

    def get_access_token(application_code: str) -> Optional[str]:
        # grant_type=authorization_code&code={APPLICATION_CODE}&redirect_uri={REDIRECT_URI}&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}

        data = {
            "grant_type": "authorization_code",
            "code": application_code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
        }
        if CLIENT_SECRET != "" and CLIENT_SECRET != None:
            data["client_secret"] = CLIENT_SECRET

        url_access_token = (
            "https://master.apis.dev.openstreetmap.org/oauth2/token"
        )
        logger.debug(data)
        r = requests.post(url=url_access_token, data=data)
        try:
            response = json.loads(r.text)
            logger.info(response)
            # response smaple
            # {'access_token': 'qwertyuiop', 'token_type': 'Bearer', 'scope': 'read_prefs write_api', 'created_at': 1145141919810}
            access_token: str = response.get("access_token", "")
            access_token_time = response.get("created_at", "")

            return access_token
        except Exception as e:
            logger.error(e)
            logger.debug(r.text)

            return None

    # step1
    oauth_login_page: str = get_oauth_login_page()
    logger.debug(oauth_login_page)

    # step2
    application_code: str = get_application_code(oauth_login_page)
    logger.debug(application_code)

    # step3
    access_token: str = get_access_token(application_code=application_code)
    logger.debug(access_token)

    return access_token
