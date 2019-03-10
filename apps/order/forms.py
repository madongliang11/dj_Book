from django import forms
from django.forms import widgets
from dj_Book.settings import PAY_CHOICES

'''
订单表单
'''
class  OrderForms(forms.Form):
	address =  forms.CharField(
      label="配送地址",
      required=True,
      widget=widgets.TextInput(
         attrs={
            "class": "form-control",
            "placeholder": "请输入配送地址",
         }),
      error_messages={
         "required": "对不起，配送地址不能为空！",
      }
   )
	pay_type = forms.ChoiceField(
      label="支付方式",
      required=True,
      choices=PAY_CHOICES,
      widget=forms.RadioSelect()
   )
	phone = forms.CharField(
      label="手机",
      required=True,
      widget=widgets.TextInput(
         attrs={
            "class": "form-control",
            "placeholder": "请输入手机",
         }),
      error_messages={
         "required": "对不起，手机不能为空！",
      }
   )