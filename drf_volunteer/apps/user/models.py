from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime
# Create your models here.

class Organ(models.Model):
    """机构表"""
    name = models.CharField(max_length=100,verbose_name="机构名", help_text="机构名")

    class Meta:
        verbose_name = '机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class UserProfile(AbstractUser):
    """
    用户表
    """
    ROLE_TYPE = (
        (0, "普通用户"),
        (1, "管理员"),
        (2, "超级管理员"),
    )

    POLITICAL_CHOICE = (
        (0, "群众"),
        (1, "共青团员"),
        (2, "中共预备党员"),
        (3, "中共党员"),
        (4, "其它党派"),

    )

    SEX_TYPE = (
        (0, "男"),
        (1, "女"),

    )

    CHECK_TYPE = (
        (0, "未审核"),
        (1, "审核通过"),
        (2, "审核未通过"),

    )

    phone = models.CharField(max_length=11,verbose_name="手机号", help_text="手机号",blank=True,null=True)

    role = models.IntegerField(choices=ROLE_TYPE, verbose_name="角色", help_text="角色",default=0)

    sex = models.IntegerField(choices=SEX_TYPE, verbose_name="性别", help_text="性别",default=0)

    political = models.IntegerField(choices=POLITICAL_CHOICE, verbose_name="政治面貌", help_text="政治面貌",default=0)

    qq = models.CharField(max_length=30,verbose_name="qq", help_text="qq",blank=True,null=True)

    weixin = models.CharField(max_length=100,verbose_name="微信", help_text="微信",blank=True,null=True)

    location = models.CharField(max_length=120,verbose_name="地址", help_text="地址",blank=True,null=True)

    mail = models.CharField(max_length=30,verbose_name="邮政编码", help_text="邮政编码",blank=True,null=True)

    logintime = models.DateTimeField(default=timezone.now(),verbose_name="注册时间", help_text="注册时间")


    check = models.IntegerField(choices=CHECK_TYPE,default=0,verbose_name="审核状态", help_text="审核状态")

    myclass = models.IntegerField(verbose_name="班级", help_text="班级",null=True,blank=True)

    organ = models.ForeignKey(Organ,verbose_name="所属组织", help_text="所属组织",related_name="user",on_delete=models.CASCADE)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username








