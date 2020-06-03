from django.db import models

from users.models import User

from .scraping import get_list_price, get_current_price

class Item(models.Model):
    """
    データ定義クラス
      各フィールドを定義する
    参考：
    ・公式 モデルフィールドリファレンス
    https://docs.djangoproject.com/ja/2.1/ref/models/fields/
    """

    # 定価
    list_price = models.IntegerField(
        verbose_name='定価',
        blank=True,
        null=True,
    )

    # 現価
    current_price = models.IntegerField(
        verbose_name='現価',
        blank=True,
        null=True,
    )

    # URL
    url = models.TextField(
        verbose_name='URL',
        blank=True,
        null=True,
    )

    # タイトル
    title = models.TextField(
        verbose_name='タイトル',
        blank=True,
        null=True,
    )

    # 作成者(ユーザー)
    created_by = models.ForeignKey(
        User,
        verbose_name='作成者',
        blank=True,
        null=True,
        related_name='CreatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )

    # 作成時間
    created_at = models.DateTimeField(
        verbose_name='作成時間',
        blank=True,
        null=True,
        editable=False,
    )

    # 更新者(ユーザー)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='UpdatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )

    # 更新時間
    updated_at = models.DateTimeField(
        verbose_name='更新時間',
        blank=True,
        null=True,
        editable=False,
    )

    '定価 取得'
    def get_price1(self):
        return get_list_price(self.url)
    
    '現価 取得'
    def get_price2(self):
        return get_current_price(self.url)
    
    def __str__(self):
        """
        リストボックスや管理画面での表示
        """
        return self.sample_1

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = 'サンプル'
        verbose_name_plural = 'サンプル'
