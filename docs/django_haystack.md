

# Django全文搜索使用

## 一 简介

> + haystack是django的开源搜索框架，该框架支持**Solr**,**Elasticsearch**,**Whoosh**, **Xapian**搜索引擎，不用更改代码，直接切换引擎，减少代码量。
> + 搜索引擎使用Whoosh，这是一个由纯Python实现的全文搜索引擎，没有二进制文件等，比较小巧，配置比较简单，当然性能自然略低。
> + 中文分词[Jieba](https://github.com/fxsjy/jieba)，由于**Whoosh**自带的是英文分词，对中文的分词支持不是太好，故用**jieba**替换**whoosh**的分词组件



## 二 安装

```python
pip install django-haystack
pip install Whoosh
pip install jieba
```



## 三 配置说明

现在假设我们的项目叫做Project,有一个apps的app下新建search_indexes.py文件(**注意**:文件名必须是这)，简略的目录结构如下:

- project

  - project
    - settings

  - apps
    - app
      - search_indexes.py

  - templates
    - search
      - indexes
        - 要索引的app名字
          - 要索引的类名(大小写都行)_text.txt
      - search.html

## 1.添加 Haystack 到Django的 INSTALLED_APPS

```python
INSTALLED_APPS = [ 
'django.contrib.admin',
'django.contrib.auth', 
'django.contrib.contenttypes', 
'django.contrib.sessions', 
'django.contrib.sites', 
# Added. haystack先添加，
'haystack', 
# Then your usual apps... 自己的app要写在haystakc后面
'blog',
```
## 2.修改 你的 settings.py，以配置引擎

> **注意:**
>
> 这里的**whoosh_cn_backend**是使用**jieba**分词器之后的
>
> 在venv/Lib/site-packages/haystack/backends/whoosh_backend.py 文件,将其修改或自己复制一份改名为whoosh_cn_backend.py (建议复制一份然后改名)

~~~python
"""
1.导入结巴中文分词器
"""
from jieba.analyse import ChineseAnalyzer
"""
2.将analyzer=StemmingAnalyzer()更改
schema_fields[field_class.index_fieldname] = TEXT(stored=True, analyzer=StemmingAnalyzer(), field_boost=field_class.boost, sortable=True)
"""
schema_fields[field_class.index_fieldname] = TEXT(stored=True, 		analyzer=ChineseAnalyzer(), field_boost=field_class.boost, sortable=True)
~~~



```python
# =================全文检索框架配置 start=============
# 搜索引擎
HAYSTACK_CONNECTIONS = {
    'default': {
        # 使用whoosh引擎
        'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine',
        # 索引文件路径
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}
# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 搜索框架
#设置每页显示的数目，默认为20，可以自己修改
HAYSTACK_SEARCH_RESULTS_PER_PAGE  = 6
# =================全文检索框架配置 end=============
```

## 3.创建索引

如果你想针对某个app做全文检索，则必须在app的目录下面建立search_indexes.py文件，文件名不能修改。内容如下此search_indexes.py的内容如下:

```python
from haystack import indexes
from apps.films.models import T_Film

#指定对于电影类的某些数据建立索引
# 注意:类名必须为要检索的Model_Name+Index
# 据模板的路径为templates/search/indexes/yourapp/note_text.txt
# note_text.txt文件名必须为要索引的类名_text.txt
class T_FilmIndex(indexes.SearchIndex,indexes.Indexable):
    # 创建一个text字段
    text = indexes.CharField(document=True,use_template=True)
    # 重载方法
    def get_model(self):
        return T_Film
    def index_queryset(self,using=None):
        return self.get_model().objects.all()	

```



## 4.在URL配置中添加SearchView，并配置模板

~~~python
url(r'^search', include('haystack.urls')),  # 全文检索框架搜索引擎url
~~~

其实`haystack.urls`的内容为

```
from django.conf.urls import url
from haystack.views import SearchView
urlpatterns = [
	url(r'^$', SearchView(), name='haystack_search'),
]
```

SearchView()视图函数默认使用的html模板路径为templates/search/search.html（再说一次推荐在根目录创建templates，并在settings.py里设置好所以需要在templates/search/下添加search.html`文件

我文件的内容为:

~~~html
{% extends 'base.html' %}
{% load staticfiles %}
{% block page_head %}
    {% include 'common/search.html' %}
{% endblock %}

{% block page_main %}
    <div class="clearfix">
    {% for item in page.object_list %}
        <ul class="pull-left list-unstyled">
            <li ><a href="{% url 'film:detail' %}?film_id={{ item.object.id }}"><img src="http://127.0.0.1:9000/{{ item.object.image }}" style="height: 300px;width: 222px;padding: 5px"></a></li>
            <h4 style="text-align: center"><a href="{% url 'film:detail' %}?film_id={{ item.object.id }}">{{ item.object.name }}</a><span style="color: orange">{{ item.object.evaluation }}</span></h4>
        </ul>
    {% endfor %}
</div>

{#    分页按钮    #}
<div class="text-center">
    <ul class="pagination ">
    {% if page.has_previous  %}
        <li><a href="/search?q={{ query }}&page={{ page.previous_page_number }}">&laquo;上一页</a></li>
    {% else %}
            <li class="disabled"><a>&laquo;上一页</a></li>
    {% endif %}
    {% for pindex in paginator.page_range %}
        <li {% if pindex == page.number %}class="active"{% endif %}><a href="/search?q={{ query }}&page={{ pindex }}" {% if pindex == page.number %}class="active"{% endif %}>{{ pindex }}</a></li>
    {% endfor %}
    {% if page.has_next %}
        <li><a href="/search?q={{ query }}&page={{ page.next_page_number }}">下一页&raquo;</a></li>
    {% else %}
            <li class="disabled"><a>下一页&raquo;</a></li>
    {% endif %}
    </ul>
</div>
{% endblock %}
~~~

很明显，它自带了分页。然后为大家解释一下这个文件。首先可以看到模板里使用了的变量有 query,page

**query:**就是我们搜索的字符串

**page:**关于page，可以看到page有object_list属性，它是一个list，里面包含了第一页所要展示的model对象集合，那么list里面到底有多少个呢？我们想要自己控制个数怎么办呢？不用担心，haystack为我们提供了一个接口。我们只要在settings.py里设置

~~~python
HAYSTACK_SEARCH_RESULTS_PER_PAGE  =  8  # 个数可以自己选
~~~



## 5.最后一步，重建索引文件

使用**python manage.py rebuild_index**或者使用**update_index**命令。好，下面运行项目，
进入该url搜索一下试试吧。每次数据库更新后都需要更新索引，所以haystack为大家提供了一个接口，
只要在settings.py里设置：

```python
#自动更新索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
```

然后你的project工程目录下就会生成whoosh_index文件夹,文件夹下会生成索引文件

![这样](C:\Users\zenglong\AppData\Local\Temp\1539403826415.png)

至此大功告成!!!!!!!!!