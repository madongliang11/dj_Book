import re

# p = re.compile('.*_(\d+)')
# now_url = 'http://www.quanshuwang.com/list/1_12.html'
# now_num = p.match(now_url).group(1)
# print(now_num)
# next_url = 'http://www.quanshuwang.com/list/1_'+p.sub('%d', now_url,count=1) % (int(now_num)+1)
# print(next_url)
#
# p = re.compile('.*(red)')
# str = "blue socks and red shoes"
# # print(type(p.sub("color",str)))

# tmp_url = 'http://www.quanshuwang.com/book_166240.html'
# num = re.match('.*?(\d+)', tmp_url).group(1)
# a = f'http://www.quanshuwang.com/book/{num[:3]}/{num}'
# print(a)
# a= 'http://www.quanshuwang.com/list/16_1.html'
# b= re.match('.*?(\d+)_.*',a).group(1)
# print(b)
# print(p.sub("color",str,count=1))

# a= 'http://www.quanshuwang.com/list/1_1.html'
# b= re.match('.*/(\d+)',a).group(1)
# print(b)

class A:
    def getname(self):
        return A.__name__

a=A()
print(a.getname())