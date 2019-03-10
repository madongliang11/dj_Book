import xadmin
# from apps.book import models
from apps.book.models import Art,Tag,Content,Chapter
from apps.user.models import ArtsUser
from xadmin import views
from apps.comment.models import Comment

class BaseSetting(object):
    # 主题修改
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    #整体配置
    site_title = '小说电商平台后台管理系统'
    site_footer = '千锋武汉python1804'
    menu_style = 'accordion'    #菜单折叠
    global_search_models = [ArtsUser, Tag,Art,Chapter, Comment]

    global_models_icon = {
        Art: "glyphicon glyphicon-book",
        Tag: "fa fa-cloud",
        Chapter:"glyphicon glyphicon-th-list",
        ArtsUser: "glyphicon glyphicon-user",
        Comment: "glyphicon glyphicon-list-alt",
        # UserMessage:  "glyphicon glyphicon-list-alt",
    }  # 设置models的全局图标


'''
标签自定义展示对象
'''
class TagAdmin(object):
    list_display = ['t_name', 't_url', 't_createtime', 't_flag']
    search_fields = ['t_name', 't_url', 't_createtime']
    list_filter = ['t_name', 't_url', 't_flag']
    list_editable = ['t_name', 't_url']



class ArtAdmin(object):
    list_display = ['id','a_title', 'a_info', 'a_author', 'a_img_url','a_img_url_figer', 'a_price' ,'a_createtime']
    search_fields = ['a_title', 'a_info','a_author']
    # list_filter = ['a_title', 'a_info', 'a_createtime', 'a_flag']
    show_detail_fields = ['a_title']
    list_per_page = 5
    list_editable = ['a_title', 'a_info', 'a_price' ,'a_author']
    style_fields = {'a_content_ue': 'ueditor'}

class ContentAdmin(object):
    list_display = ['id','a_content']
    search_fields = ['a_content']
    list_per_page = 5

class CapterAdmin(object):
    list_display = ['id', 'title', 'content', 'create_time']
    search_fields = [ 'title', 'content', 'create_time']
    list_filter = [ 'title', 'content', 'create_time']
    list_per_page = 5

class CommentAdmin(object):
    list_display = ['name', 'title', 'text', 'created_time', 'book', 'flag']
    search_fields =  ['name', 'title', 'text', 'created_time', 'book']
    list_per_page = 5


xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(views.BaseAdminView, BaseSetting)


xadmin.site.register(ArtsUser)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Art, ArtAdmin)
xadmin.site.register(Content, ContentAdmin)
xadmin.site.register(Chapter, CapterAdmin)
xadmin.site.register(Comment, CommentAdmin)