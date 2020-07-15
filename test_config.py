from typing import Protocol
import yaml
import toml

txt_yaml = """
site:
    port: 80
    pages: [homepage, about]
    cached: true
lang:
    en:
        homepage: homepage
        about: about
    cn:  
        homepage : 主页
        about : 关于        
"""

txt_toml = """
[site]
port = 80
pages=['homepage','about']
cached = true

[lang.en]
homepage = 'homepage'
about = 'about'

[lang.cn]
homepage = '主页'
about = '关于'
"""


def assert_data(data):
    site = data['site']
    assert(site['port'] == 80)
    assert(len(site['pages']) == 2)
    lang_cn = data['lang']['cn']
    assert(lang_cn['about'] == '关于')


def test_yaml():
    data = yaml.full_load(txt_yaml)
    assert_data(data)
    print(yaml.dump(data))


def test_toml():
    data = toml.loads(txt_toml)
    assert_data(data)
    print(toml.dumps(data))


test_yaml()
test_toml()
