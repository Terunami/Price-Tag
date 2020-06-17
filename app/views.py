import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from .filters import ItemFilterSet
from .forms import ItemForm
from .models import Item

# スクレイピングで定価、現価を取得
from .scraping import playstation
# HTTPメソッドをPOSTに制限するデコレータ
from django.views.decorators.http import require_POST
# HTMLを部分的に返すため
from django.http import HttpResponse
# GOOGLE検索結果をjsonで取得
from .get_search_response import getSearchResponse
import json

# 未ログインのユーザーにアクセスを許可する場合は、LoginRequiredMixinを継承から外してください。
#
# LoginRequiredMixin：未ログインのユーザーをログイン画面に誘導するMixin
# 参考：https://docs.djangoproject.com/ja/2.1/topics/auth/default/#the-loginrequired-mixin

class ItemFilterView(LoginRequiredMixin, FilterView):
    """
    ビュー：一覧表示画面

    以下のパッケージを使用
    ・django-filter 一覧画面(ListView)に検索機能を追加
    https://django-filter.readthedocs.io/en/master/
    """
    model = Item

    # django-filter 設定
    filterset_class = ItemFilterSet
    # django-filter ver2.0対応 クエリ未設定時に全件表示する設定
    strict = False

    # 1ページの表示
    paginate_by = 10


    def get(self, request, **kwargs):
        """
        リクエスト受付
        セッション変数の管理:一覧画面と詳細画面間の移動時に検索条件が維持されるようにする。
        """

        # 一覧画面内の遷移(GETクエリがある)ならクエリを保存する
        if request.GET:
            request.session['query'] = request.GET
        # 詳細画面・登録画面からの遷移(GETクエリはない)ならクエリを復元する
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)

    def get_queryset(self):
        """
        ソート順・デフォルトの絞り込みを指定
        """
        # デフォルトの並び順として、登録時間（降順）をセットする。
        return Item.objects.all().order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        表示データの設定
        """
        # 表示データを追加したい場合は、ここでキーを追加しテンプレート上で表示する
        # 例：kwargs['sample'] = 'sample'
        return super().get_context_data(object_list=object_list, **kwargs)


class ItemDetailView(LoginRequiredMixin, DetailView):
    """
    ビュー：詳細画面
    """
    model = Item

    def get_context_data(self, **kwargs):
        """
        表示データの設定
        """
        # 表示データの追加はここで 例：
        # kwargs['sample'] = 'sample'
        return super().get_context_data(**kwargs)


class ItemCreateView(LoginRequiredMixin, CreateView):
    """
    ビュー：登録画面
    """
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """
        登録処理
        """
        item = form.save(commit=False)
        item.created_by = self.request.user
        item.created_at = timezone.now()
        item.updated_by = self.request.user
        item.updated_at = timezone.now()
        item.save()

        return HttpResponseRedirect(self.success_url)


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    """
    ビュー：更新画面
    """
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """
        更新処理
        """
        item = form.save(commit=False)
        item.updated_by = self.request.user
        item.updated_at = timezone.now()
        item.save()

        return HttpResponseRedirect(self.success_url)


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    """
    ビュー：削除画面
    """
    model = Item
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        """
        削除処理
        """
        item = self.get_object()
        item.delete()

        return HttpResponseRedirect(self.success_url)


class ItemPriceUpdateView(LoginRequiredMixin, UpdateView):

    model = Item
    form_class = ItemForm
    # template_name = ''
    
    def price_update(request):
        """
        値段更新処理
        """
        success_url = reverse_lazy('index')
        
        item_id = request.POST.getlist('item_id')[0]
        item = Item.objects.all().get(id=item_id)
        item.list_price = ItemPriceUpdateView.get_price1(item)
        item.current_price = ItemPriceUpdateView.get_price2(item)
        # item.updated_by = item.request.user
        item.updated_at = timezone.now()
        item.save()

        return HttpResponseRedirect(success_url)
    
    '定価 取得'
    def get_price1(self):
        return playstation.get_list_price(self.url)
    
    '現価 取得'
    def get_price2(self):
        return playstation.get_current_price(self.url)



class ItemSearchCreateView(LoginRequiredMixin, CreateView):

    def search_title(request):
        title = request.POST.getlist("game_title")
        site = 'https://store.playstation.com/ja-jp/product/'
        response = json.loads(getSearchResponse('intitle:{title} site:{site}'.format(title=title ,site=site)))

        button_html = ""
        # submit_button = ""
        with open('app/templates/app/label_button.html') as f:
            button_html = f.read()
        # with open('app/templates/app/submit_button.html') as f:
        #     submit_html = f.read()

        html_text = ""
        id_num = 0

        if int(response['response'][0]['searchInformation']['totalResults']) > 0:

            for result in response['response'][0]['items']:
                title = result['title']
                link = result['link']
                html_text += button_html.format(link=link, title=title, id_num=id_num)
                id_num+=1
            # html_text += submit_html
        else:

            html_text = "<p>タイトルを入力してください<p>"

        return HttpResponse(html_text)

    def create_item(request):

        model = Item
        form_class = ItemForm
        success_url = reverse_lazy('index')

        title = request.POST.getlist("title")[0]
        radio_num = request.POST.getlist("radio_num")[0]
        url = request.POST.getlist("link")[int(radio_num)]

        list_price = playstation.get_list_price(url)
        current_price = playstation.get_current_price(url)
        created_at = timezone.now()
        updated_at = timezone.now()

        Item.objects.create(title=title, url=url, list_price=list_price, current_price=current_price, created_at=created_at, updated_at=updated_at)
        print("create")
        return HttpResponseRedirect(success_url)






