"""
@Author：WangYuXiang
@E-mile：Hill@3io.cc
@CreateTime：2021/3/11 17:37
@DependencyLibrary：无
@MainFunction：无
@FileDoc： 
    paginations.py
    分页器
@ChangeHistory:
    datetime action why
    example:
    2021/3/11 17:37 change 'Fix bug'
        
"""
from sanic.request import Request
from tortoise import Model

from sanic_rest_framework.exceptions import APIException
from sanic_rest_framework.status import HttpStatus
from sanic_rest_framework.utils import replace_query_param


class BasePagination:
    """抽象基类"""

    async def paginate_queryset(self, queryset, request, view):
        raise NotImplementedError(
            '必须在 `%s` 中实现异步的 `.paginate_queryset()` 方法' % self.__class__.__name__)

    def response(self, request, data):
        raise NotImplementedError(
            '必须在 `%s` 中实现 `.response()` 方法' % self.__class__.__name__)


class GeneralPagination(BasePagination):
    """通用分页器"""
    page_size = 60
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 10000

    @property
    def count(self):
        """总记录数"""
        assert hasattr(self, '_count'), '必须先执行 `.paginate_queryset()` 函数才能使用.count'
        return self._count

    def get_next_link(self, request: Request):
        """
        得到下一页的请求地址
        :param request:
        :return: None or String
        """
        assert hasattr(self, '_count'), '必须先执行 `.paginate_queryset()` 函数才能使用.get_next_link()'
        page = self.get_next_page()
        if not page:
            return None
        uri = request.server_path
        query_string = '?' + request.query_string
        query_string = replace_query_param(query_string, self.page_query_param, page)
        query_string = replace_query_param(query_string, self.page_size_query_param, self.page_size)
        return uri + query_string

    def get_next_page(self):
        """得到下一页的页码，不存在则返回None"""
        if self.page * self.page_size + self.page_size >= self.count:
            return None
        return self.page + 1

    def get_previous_link(self, request: Request):
        """
        得到上一页的请求地址
        :param request:
        :return: None or String
        """
        assert hasattr(self, '_count'), '必须先执行 `.paginate_queryset()` 函数才能使用.get_previous_link()'
        page = self.get_previous_page()
        if not page:
            return None
        uri = request.server_path
        query_string = '?' + request.query_string
        query_string = replace_query_param(query_string, self.page_query_param, page)
        query_string = replace_query_param(query_string, self.page_size_query_param, self.page_size)
        return uri + query_string

    def get_previous_page(self):
        """得到上一页页码，不存在则返回None"""
        if self.page * self.page_size <= 0:
            return None
        return self.page - 1

    async def paginate_queryset(self, queryset, request, view):
        """为queryset添加分页查询条件"""
        self.page = self.get_query_page(request)
        self.page_size = self.get_query_page_size(request)
        if not isinstance(queryset, Model):
            queryset = queryset.filter()
        self._count = await queryset.count()
        return queryset.limit(self.page_size).offset((self.page - 1) * self.page_size)

    def get_query_page(self, request):
        """得到页数"""
        try:
            page = int(request.args.get(self.page_query_param, 1))
        except ValueError as exc:
            raise APIException('发生错误的分页数据', http_status=HttpStatus.HTTP_400_BAD_REQUEST)
        if page < 1:
            page = 1
        return page

    def get_query_page_size(self, request):
        """得到页记录数"""
        try:
            page = int(request.args.get(self.page_size_query_param, self.page_size))
            if page > self.max_page_size:
                raise APIException('分页内容大小超出最大限制', http_status=HttpStatus.HTTP_400_BAD_REQUEST)
        except ValueError as exc:
            raise APIException('发生错误的分页数据', http_status=HttpStatus.HTTP_400_BAD_REQUEST)
        return page

    def response(self, request, data):
        """便捷的response"""
        return {
            'count': self.count,
            'next': self.get_next_link(request),
            'previous': self.get_previous_link(request),
            'results': data,
        }
