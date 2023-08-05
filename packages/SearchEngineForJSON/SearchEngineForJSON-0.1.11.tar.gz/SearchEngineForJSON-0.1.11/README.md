
# SearchEngine for JSON (自作パッケージ公開)
* json形式のデータから条件に従ったkeyとvalueを再起的に取得します

[![Downloads](https://pepy.tech/badge/searchengineforjson)](https://pepy.tech/project/searchengineforjson)
[![Downloads](https://pepy.tech/badge/searchengineforjson/month)](https://pepy.tech/project/searchengineforjson)
[![Downloads](https://pepy.tech/badge/searchengineforjson/week)](https://pepy.tech/project/searchengineforjson)


<img alt="Run pytest" src="https://github.com/aoimaru/packagingTutorial/workflows/Upload Python Package/badge.svg"></a>
# install
```bash
pip install SearchEngineForJSON
```
## ディレクトリ構造
```
|--packagingTutorial
|  |--SearchEngineForJSON
|  |  |--__init__.py
|  |  |--search.py
|  |--setup.py
```

# Usage
```
import SearchEngineForJSON


SearchEngineForJSON.Search.typeSearch(探索したいデータ, 探索したい型) -> [[key, value],...,[]]
SearchEngineForJSON.Search.getAll(探索したいデータ) -> [[key, value],...,[]]
SearchEngineForJSON.Search.valueSearch(探索したいデータ, 探索したい値) -> [[key, value],...,[]]
SearchEngineForJSON.Search.subValueSearch(探索したいデータ, 探索したい値の部分文字列) -> [[key, value],...,[]]
SearchEngineForJSON.Search.startValueSearch(探索したいデータ, 探索したい値の先頭文字列) -> [[key, value],...,[]]
SearchEngineForJSON.Search.endValueSearch(探索したいデータ, 探索したい値の末尾文字列) -> [[key, value],...,[]]
SearchEngineForJSON.Search.keySearch(探索したいデータ, 探索したいキー) -> [[key, value],...,[]]
SearchEngineForJSON.Search.subKeySearch(探索したいデータ, 探索したいキーの部分文字列) -> [[key, value],...,[]]
```

# Example
```
import SearchEngineForJSON

data = {
    "name1": "Nakamura",
    "name2": {
        "name2-1": "Aoi",
        "name2-2": [
            "listA",
            "listB",
            {
                True: "listInDict1",
                2: "listInDict2",
                2.2: {
                    "listC-3-1": "hello",
                    "listC-3-2": "world",
                    "listC-3-3": [
                        "Sunday",
                        "Monday",
                        "Tuesday"
                    ],
                    "listC-3-4": 5,
                    "listC-3-5": True,
                    "listC-3-6": False,
                    "listC-3-7": None
                },
                "->": "listInDict3",
                "->->": "listInDict4",
                "->->->": "listInDict5",
                "->hello": "listInDict6",
                "hello->": "listInDict7",
                "->hello->": "listInDict8",
                "he->llo": [
                    "in",
                    "out"
                ],
                "2.2": "string",
                "2.3": 2,
                "2.4": 2.2,
                "2.5": "listInDict6"
            },
            "listD",
            "listE"
        ],
        "name2-3": "python",
        "name2-4": [
            "Docker",
            "kubernetes",
            "Docker-compose"
        ]
    },
    "name3": "json",
    "name4": "search"
}

```
```
typeSearchAnswer = SearchEngineForJSON.Search.typeSearch(data, str)

typeSearchAnswer = [
    ['name1', 'Nakamura'],
    ['name3', 'json'],
    ['name4', 'search'],
    ['name2->name2-1', 'Aoi'],
    ['name2->name2-3', 'python'],
    ['name2->name2-2->list(0)', 'listA'],
    ['name2->name2-2->list(1)', 'listB'],
    ['name2->name2-2->list(3)', 'listD'],
    ['name2->name2-2->list(4)', 'listE'],
    ['name2->name2-2->list(2)->bool(True)', 'listInDict1'],
    ['name2->name2-2->list(2)->int(2)', 'listInDict2'],
    ['name2->name2-2->list(2)->(>)', 'listInDict3'],
    ['name2->name2-2->list(2)->(>)(>)', 'listInDict4'],
    ['name2->name2-2->list(2)->(>)(>)(>)', 'listInDict5'],
    ['name2->name2-2->list(2)->(>)hello', 'listInDict6'],
    ['name2->name2-2->list(2)->hello(>)', 'listInDict7'],
    ['name2->name2-2->list(2)->(>)hello(>)', 'listInDict8'],
    ['name2->name2-2->list(2)->2.2', 'string'],
    ['name2->name2-2->list(2)->2.5', 'listInDict6'],
    ['name2->name2-2->list(2)->float(2.2)->listC-3-1', 'hello'],
    ['name2->name2-2->list(2)->float(2.2)->listC-3-2', 'world'],
    ['name2->name2-2->list(2)->float(2.2)->listC-3-3->list(0)', 'Sunday'],
    ['name2->name2-2->list(2)->float(2.2)->listC-3-3->list(1)', 'Monday'],
    ['name2->name2-2->list(2)->float(2.2)->listC-3-3->list(2)', 'Tuesday'],
    ['name2->name2-2->list(2)->he(>)llo->list(0)', 'in'],
    ['name2->name2-2->list(2)->he(>)llo->list(1)', 'out'],
    ['name2->name2-4->list(0)', 'Docker'],
    ['name2->name2-4->list(1)', 'kubernetes'],
    ['name2->name2-4->list(2)', 'Docker-compose'],
]
```
```
getAllAnswear = SearchEngineForJSON.Search.getAll(data)

getAllAnswear = [
    ['name1', 'Nakamura'],
    ['name3', 'json'],
    ['name4', 'search'],
    ['name2->name2-1', 'Aoi'],
    ['name2->name2-3', 'python'],
    ['name2->name2-2->list(0)', 'listA'],
    ['name2->name2-2->list(1)', 'listB'],
    ['name2->name2-2->list(3)', 'listD'],
    ['name2->name2-2->list(4)', 'listE'],
    ['name2->name2-2->list(2)->bool(True)', 'listInDict1'],
    ['name2->name2-2->list(2)->int(2)', 'listInDict2'],
    ['name2->name2-2->list(2)->(>)', 'listInDict3'],
    ['name2->name2-2->list(2)->(>)(>)', 'listInDict4'],
    ['name2->name2-2->list(2)->(>)(>)(>)', 'listInDict5'],
    ['name2->name2-2->list(2)->(>)hello', 'listInDict6'],
    ['name2->name2-2->list(2)->hello(>)', 'listInDict7'],
    ['name2->name2-2->list(2)->(>)hello(>)', 'listInDict8'],
    ['name2->name2-2->list(2)->2.2', 'string'],
    ['name2->name2-2->list(2)->2.3', 2],
    ['name2->name2-2->list(2)->2.4', 2.2],
    ['name2->name2-2->list(2)->2.5', 'listInDict6'],
    ['name2->name2-2->list(2)->float(2.2)->listC-3-1', 'hello'],
    ['name2->name2-2->list(2)->float(2.2)->listC-3-2', 'world'],
    ['name2->name2-2->list(2)->float(2.2)->listC-3-4', 5],
    ['name2->name2-2->list(2)->float(2.2)->listC-3-5', True],
    ['name2->name2-2->list(2)->float(2.2)->listC-3-6', False],
    ['name2->name2-2->list(2)->float(2.2)->listC-3-7', None],
    ['name2->name2-2->list(2)->float(2.2)->listC-3-3->list(0)', 'Sunday'],
    ['name2->name2-2->list(2)->float(2.2)->listC-3-3->list(1)', 'Monday'],
    ['name2->name2-2->list(2)->float(2.2)->listC-3-3->list(2)', 'Tuesday'],
    ['name2->name2-2->list(2)->he(>)llo->list(0)', 'in'],
    ['name2->name2-2->list(2)->he(>)llo->list(1)', 'out'],
    ['name2->name2-4->list(0)', 'Docker'],
    ['name2->name2-4->list(1)', 'kubernetes'],
    ['name2->name2-4->list(2)', 'Docker-compose']
]
```
```
valueSearchAnswear = SearchEngineForJSON.Search.valueSearch(data, "listInDict6")

valueSearchAnswear = [
    ['name2->name2-2->list(2)->(>)hello', 'listInDict6'],
    ['name2->name2-2->list(2)->2.5', 'listInDict6']
]
```
```
subValueSearchAnswear = SearchEngineForJSON.Search.subValueSearch(data, "list")

subValueSearchAnswear = [
    ['name2->name2-2->list(0)', 'listA'],
    ['name2->name2-2->list(1)', 'listB'],
    ['name2->name2-2->list(3)', 'listD'],
    ['name2->name2-2->list(4)', 'listE'],
    ['name2->name2-2->list(2)->bool(True)', 'listInDict1'],
    ['name2->name2-2->list(2)->int(2)', 'listInDict2'],
    ['name2->name2-2->list(2)->(>)', 'listInDict3'],
    ['name2->name2-2->list(2)->(>)(>)', 'listInDict4'],
    ['name2->name2-2->list(2)->(>)(>)(>)', 'listInDict5'],
    ['name2->name2-2->list(2)->(>)hello', 'listInDict6'],
    ['name2->name2-2->list(2)->hello(>)', 'listInDict7'],
    ['name2->name2-2->list(2)->(>)hello(>)', 'listInDict8'],
    ['name2->name2-2->list(2)->2.5', 'listInDict6']
]
```
```
startValueSearchAnswear = SearchEngineForJSON.Search.startValueSearch(data, "listIn")

startValueSearchAnswear = [
    ['name2->name2-2->list(2)->bool(True)', 'listInDict1'],
    ['name2->name2-2->list(2)->int(2)', 'listInDict2'],
    ['name2->name2-2->list(2)->(>)', 'listInDict3'],
    ['name2->name2-2->list(2)->(>)(>)', 'listInDict4'],
    ['name2->name2-2->list(2)->(>)(>)(>)', 'listInDict5'],
    ['name2->name2-2->list(2)->(>)hello', 'listInDict6'],
    ['name2->name2-2->list(2)->hello(>)', 'listInDict7'],
    ['name2->name2-2->list(2)->(>)hello(>)', 'listInDict8'],
    ['name2->name2-2->list(2)->2.5', 'listInDict6']
]
```
```
endValueSearchAnswear = SearchEngineForJSON.Search.endValueSearch(data, "Dict6")

endValueSearchAnswear = [
    ['name2->name2-2->list(2)->(>)hello', 'listInDict6'],
    ['name2->name2-2->list(2)->2.5', 'listInDict6']
]
```

```
keySearchAnswear = SearchEngineForJSON.Search.keySearch(data, "2.5")

keySearchAnswear = [
    ['name2->name2-2->list(2)->2.5', 'listInDict6']
]
```
```
subKeySearchAnswear = SearchEngineForJSON.Search.subKeySearch(data, "stC-3-")

subKeySearchAnswear = [
    ['name2->name2-2->list(2)->float(2.2)->listC-3-1', 'hello'],
    ['name2->name2-2->list(2)->float(2.2)->listC-3-2', 'world'],
    ['name2->name2-2->list(2)->float(2.2)->listC-3-3', ['Sunday', 'Monday', 'Tuesday']],
    ['name2->name2-2->list(2)->float(2.2)->listC-3-4', 5],
    ['name2->name2-2->list(2)->float(2.2)->listC-3-5', True],
    ['name2->name2-2->list(2)->float(2.2)->listC-3-6', False],
    ['name2->name2-2->list(2)->float(2.2)->listC-3-7', None]
]
```
