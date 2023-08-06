# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mbd_pay']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1,<2.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'mbd-pay',
    'version': '0.1.4',
    'description': '面包多支付SDK - https://mbd.pub/',
    'long_description': '# mbd-pay\n\n\n[面包多Pay文档](https://doc.mbd.pub/)\n- 封装签名、请求参数与返回值，具体结构参考 [types.py](https://github.com/shaoxyz/mbd_pay/blob/dev/mbd_pay/types.py)\n- 支持所有[requests](https://docs.python-requests.org/en/master/)库执行请求时支持的参数，比如 `timeout`\n\n\n## Quickstart\n\nInstall using `pip`:\n\n```shell\n$ pip install mbd-pay\n```\n## Example\n```python\nfrom mbd_pay import Client\n\nc = Client(app_id="**", app_key="**")\n\n# 生成获取openid的链接\nprint("openid_redirect_url: \\n", c.get_openid_redirect_url(target_url="baidu.com"))\n\nprint(\n    "wx jsapi: \\n",\n    c.wx_jsapi(\n        openid="123", description="321", amount_total=100, callback_url="baidu.com"，\n    ),\n)\n\nprint("wx h5: \\n", c.wx_h5(description="321", amount_total=100))\n\nprint("alipay: \\n", c.alipay(url="baidu.com", description="321", amount_total=100))\n\nprint("refund: \\n", c.refund(order_id="123"))\n\nprint("search order: \\n", c.search_order(out_trade_no="123"))\n\n```\n\n## Reference\n```python\ndef _handle_req(self, req) -> dict:\n    """\n    `req` Model to dict, and add sign | 过滤空值、签名、构建请求体\n    """\n    req = req.dict(exclude_none=True)\n    req.update(app_id=self.app_id)\n    req.update(sign=sign(req, self.app_key))\n    return req\n        \ndef _post(self, _url: str, req, **kwargs):\n    """\n    build request body for POST, split out requests\' kwargs\n    :param url: url\n    :param req: see ***Req in types.py\n    :param kwargs: req + `requests.post`\'s kwargs, e.g. timeout=5\n    :return:\n    """\n    body = self._handle_req(req)\n\n    # split out requests\' kwargs | 抽离出所有面包多Pay以外的参数，并传递给requests执行实际请求\n    other_kwargs = {\n        i: kwargs[i] for i in kwargs.keys() if i not in req.__fields_set__\n    }\n\n    return requests.post(_url, json=body, **other_kwargs).json()\n        \ndef wx_jsapi(self, **kwargs) -> WeChatJSApiRes:\n    """\n    see：https://doc.mbd.pub/api/wei-xin-zhi-fu\n    :param kwargs: WeChatJSApiReq required fields\n        and optional `requests.post`\'s kwargs, e.g. timeout=5\n    :return: WeChatJSApiRes\n    """\n    req = WeChatJSApiReq(**kwargs)  # 用kwarg实例化一个WeChatJSApiReq对象\n    api = f"{self.domain}/release/wx/prepay"\n    res = self._post(api, req, **kwargs)\n\n    return WeChatJSApiRes(**res)  # 用返回值实例化一个WeChatJSApiRes对象\n```\n\n## Thanks\n  - [Requests](https://docs.python-requests.org/en/master/)\n  - [Pydantic](https://pydantic-docs.helpmanual.io/)\n\n## Todos\n\n - WebHooks\n\nLicense\n----\n\nMIT\n\n\n**Hell Yeah!**\n\n',
    'author': 'shaoxyz',
    'author_email': 'shwb95@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shaoxyz/mbd_pay',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
