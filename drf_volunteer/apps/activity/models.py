from django.db import models
from apps.user.models import UserProfile,Organ
from DjangoUeditor.models import UEditorField

from django.utils import timezone

import datetime
# Create your models here.


class Type(models.Model):
    """类型"""
    name = models.CharField(max_length=100, verbose_name="类型名", help_text="类型名")

    class Meta:
        verbose_name = '类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name




class Ativity(models.Model):
    """义工活动表"""
    STATUS = (
        (0,"待审核"),
        (1,"审核中"),
        (2,"待发布"),
        (3,"已发布"),
        (4,"报名中"),
        (5,"报名结束"),
        (6,"活动中"),
        (7,"活动结束"),
        (8,"活动取消"),
        (9,"时长已录入"),
        (10,"审核不通过"),
    )

    title = models.CharField(max_length=100,verbose_name="标题", help_text="标题")

    registration_time = models.DateField(verbose_name="报名时间", help_text="报名时间",blank=True,null=True)

    activity_time = models.IntegerField(verbose_name="活动时长", help_text="活动时长")

    link_phone = models.CharField(max_length=11,verbose_name="联系电话", help_text="联系电话")

    link_pople = models.CharField(max_length=20,verbose_name="联系人", help_text="联系人")

    activity_content = UEditorField(verbose_name="活动内容", help_text="活动内容", null=True, blank=True,filePath='ueditor/file/',imagePath='ueditor/images/')

    organ = models.ForeignKey(Organ,on_delete=models.CASCADE,verbose_name="机构", help_text="机构",related_name="activity")

    people_count = models.IntegerField(default=100,verbose_name="招募人数", help_text="招募人数")

    activity_starttime = models.DateTimeField(verbose_name="活动时间", help_text="活动时间")

    address = models.CharField(max_length=300,blank=True,null=True)

    people = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name="创建人", help_text="创建人",related_name="acivity")

    status = models.IntegerField(choices=STATUS,verbose_name="活动状态", help_text="活动状态",default=0)

    createtime = models.DateTimeField(default=datetime.datetime.now(),verbose_name="创建时间", help_text="创建时间")

    updatetime = models.DateTimeField(auto_now=True,verbose_name="最后修改时间", help_text="最后修改时间")

    hot = models.ManyToManyField(UserProfile,related_name="my_like", help_text="喜欢人",verbose_name="喜欢人", blank=True, null=True)

    hotcount = models.IntegerField(default=0)

    user = models.ManyToManyField(UserProfile, through="UserandActivity", related_name="my_match", help_text="报名人",
                                  verbose_name="报名人", blank=True, null=True)

    type = models.ForeignKey(Type,related_name="actiyity", help_text="类型",verbose_name="类型",on_delete=models.CASCADE,blank=True,null=True)

    no_check = models.CharField(max_length=200, verbose_name="不通过意见", help_text="不通过意见", null=True, blank=True)

    activity_pic = models.FileField(verbose_name="活动图片", help_text="活动图片", blank=True, null=True, upload_to="activitypic/")
    class Meta:
        verbose_name = '义工活动'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tiile

class UserandActivity(models.Model):
    """用户活动表"""
    RANK = (
        (0,"差"),
        (1,"一般"),
        (2,"优秀")
    )

    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="user",verbose_name="活动人", help_text="活动人")

    activity = models.ForeignKey(Ativity,on_delete=models.CASCADE,related_name="activity",verbose_name="活动", help_text="活动")

    rank = models.IntegerField(choices=RANK,blank=True,null=True,verbose_name="等级", help_text="等级")

    activity_time = models.IntegerField(default=0,verbose_name="义工时", help_text="义工时")

    signtime = models.DateTimeField(default=timezone.now(),verbose_name="报名时间", help_text="报名时间")



class Histroy(models.Model):
    """历史活动"""
    activity = models.OneToOneField(Ativity,on_delete=models.CASCADE,verbose_name="义工", help_text="义工")

    title = models.CharField(max_length=20,verbose_name="题目", help_text="题目")

    content = UEditorField(verbose_name="活动内容", help_text="活动内容", null=True, blank=True,filePath='ueditor/file/',imagePath='ueditor/images/')

    createtime = models.DateTimeField(default=datetime.datetime.now(),verbose_name="创建时间", help_text="创建时间")

    updatetime = models.DateTimeField(auto_now=True, verbose_name="最后修改时间", help_text="最后修改时间")

    publishtime = models.DateTimeField(null=True, blank=True, verbose_name="发布时间", help_text="发布时间")

    class Meta:
        verbose_name = '历史活动'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tiile


class HPic(models.Model):
    """Histroy"""
    url = models.FileField(verbose_name="历史图片", help_text="历史图片", blank=True, null=True, upload_to="historypic/")

    histroy = models.ForeignKey(Histroy,on_delete=models.CASCADE,related_name="pic")


class Community(models.Model):
    """社区"""
    title = models.CharField(max_length=100,verbose_name="标题", help_text="标题")

    content = UEditorField(verbose_name="活动内容", help_text="活动内容", null=True, blank=True, filePath='ueditor/file/',
                           imagePath='ueditor/images/')

    createtime = models.DateTimeField(default=datetime.datetime.now(), verbose_name="创建时间", help_text="创建时间")

    updatetime = models.DateTimeField(auto_now=True, verbose_name="最后修改时间", help_text="最后修改时间")

    publishtime = models.DateTimeField(null=True,blank=True, verbose_name="发布时间", help_text="发布时间")

    publishuser = models.ForeignKey(UserProfile,related_name="publish",on_delete=models.CASCADE,null=True,blank=True, verbose_name="发布者", help_text="发布者")
    class Meta:
        verbose_name = '社区'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tiile


class Communitypic(models.Model):
    """社区图片"""
    url = models.FileField(verbose_name="比赛结果", help_text="比赛结果", blank=True, null=True, upload_to="communitypic/")

    community = models.ForeignKey(Community,on_delete=models.CASCADE,related_name="pic")

