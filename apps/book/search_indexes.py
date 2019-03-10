from haystack import indexes
from apps.book.models import Art

#指定对于电影类的某些数据建立索引
# 注意:类名必须为要检索的Model_Name+Index
# 据模板的路径为templates/search/indexes/yourapp/note_text.txt
# note_text.txt文件名必须为要索引的类名_text.txt

class ArtIndex(indexes.SearchIndex,indexes.Indexable):
    # 创建一个text字段
    text = indexes.CharField(document=True,use_template=True)

    # 重载方法
    def get_model(self):
        return Art

    def index_queryset(self,using=None):
        art_model = self.get_model().objects.all()
        print(art_model)
        return art_model


