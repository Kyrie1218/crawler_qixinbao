from ..toollib.bs import _to_bs
from ..config import config
import os

vote_up = config.get('vote_up')


def _get_author_info(bs_obj):
    ret = bs_obj.find('div', {'class': 'AuthorInfo'}).find_all('a')
    if ret:
        return ret[-1]
    return '匿名用户'


def _get_author_name(bs_obj):
    ret = _get_author_info(bs_obj)
    if ret == '匿名用户':
        return '匿名用户'
    return ret.text


def _get_author_url(bs_obj):
    ret = _get_author_info(bs_obj)
    if ret == '匿名用户':
        return ''
    return ret.get('href')


def _get_attr(bs_obj):
    return _get_author_name(bs_obj), _get_author_url(bs_obj), _get_vote(bs_obj)


def _get_vote(bs_obj):
    vote = bs_obj.find('button', {'class': 'VoteButton--up'}).text
    if vote.isdigit():
        return int(bs_obj.find('button', {'class': 'VoteButton--up'}).text)
    if 'K' in vote:
        return int(float(vote.strip('K')) * 1000)
    return 0


def _get_images(answer):
    noscripts = answer.find_all('noscript')
    if noscripts:
        images = []
        for item in noscripts:
            bs_obj = _to_bs('<' + item.text.strip('&gt;').strip('lt;') + '/>')  # convert noscripts element to img
            src, width, height = bs_obj.img.attrs.get('src').replace('_b', ''), bs_obj.img.attrs.get(
                'data-rawwidth'), bs_obj.img.attrs.get('data-rawheight')
            images.append((src, width, height))
        return images
    return noscripts


def _get_answers(bs_obj):
    ret = []
    for item in bs_obj.find_all('div', {'class': 'List-item'}):
        if len(item.attrs.get('class')) == 1:
            ret.append(item)
    return ret


def _filter_answer(bs_obj):
    if _get_vote(bs_obj) < vote_up:
        return
    images = _get_images(bs_obj)
    if not images:
        return
    return images



#   def filter_tags(self, htmlstr):
#     print(htmlstr)
#     return
#     #先过滤CDATA
#     # re_cdata   = re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
#     # re_script  = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
#     # re_style   = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
#     # re_br      = re.compile('<br\s*?/?>')#处理换行
#     re_h       = re.compile('</?\w+[^>]*>')#HTML标签
#     # re_comment = re.compile('<!--[^>]*-->')#HTML注释
#     # html          = re_cdata.sub('',htmlstr)#去掉CDATA


#     # html          = re_script.sub('',html) #去掉SCRIPT
#     # html          = re_style.sub('',html)#去掉style
#     # html          = re_br.sub('\n',html)#将br转换为换行
#     html          = re_h.sub('',htmlstr) #去掉HTML 标签
#     # html          = re_comment.sub('',html)#去掉HTML注释
#     #去掉多余的空行
#     # blank_line = re.compile('\n+')
#     # html          = blank_line.sub('\n',html)

#     return html
