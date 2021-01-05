from apps.activity.views import *
from django.urls import path

# 超管
adminacivity_urls = AdminAcivityViewset.as_view()

# 老师操作
acivity_urls = AcivityViewset.as_view({
    "get": "list",
    "post": "create",
    "put": "update",
})

acivity_detail_urls = AcivityViewset.as_view({
    "get": "retrieve",
    "delete": "destroy"
})

admin_organ_urls = AdminorganViewset.as_view()

type_urls = TypeViewset.as_view({
    "get": "list",
    "post": "create",
    "put": "update",
})

type_detail_urls = TypeViewset.as_view({
    "get": "retrieve",
    "delete": "destroy"
})

acivitystatus_urls_urls = ActivityStatusViewset.as_view()

community_urls = CommunityViewset.as_view({
    "get": "list",
    "post": "create",
    "put": "update"
})

community_detail_urls = CommunityViewset.as_view({
    "get": "retrieve",
    "delete": "destroy"
})

communitypic_urls = CommunityPicViewset.as_view()

history_urls = HistroyViewset.as_view({
    "get": "list",
    "post": "create",
    "put": "update"
})

history_detail_urls = HistroyViewset.as_view({
    "get": "retrieve",
    "delete": "destroy"
})

# 义工时逻辑
activitytime_urls = ActivityTimeViewset.as_view()

historypic_urls = HistroyPicViewset.as_view({
    "post": "create",
    "delete": "destory"
})

# 分析
analyse_urls = AnalyseViewset.as_view()

# 学生操作
sturegacivity_urls = StuRegAcivityViewset.as_view({
    "get": "list",
    "post": "create",
})

sturegacivity_detail_urls = StuRegAcivityViewset.as_view({
    "get": "retrieve",
    "delete": "destroy"
})

stuacivity_urls = StuAcivityViewset.as_view({
    "get": "list",
    "post": "create",
})

stuacivity_detail_urls = StuAcivityViewset.as_view({
    "get": "retrieve",
    "delete": "destroy"
})

stuhistory_urls = StuHistoryViewset.as_view({
    "get": "list",

})

stucommunity_urls = StuCommunityViewset.as_view({
    "get": "list",

})

passstu_urls = GetPassStudentViewset.as_view()

urlpatterns = [
    # 超管
    path("admin/activity/", adminacivity_urls),
    path("admin/organ/", admin_organ_urls),
    # 教师逻辑
    path("activity/", acivity_urls),
    path("activity/<int:pk>/", acivity_detail_urls),
    path("activity/status/", acivitystatus_urls_urls),

    path("activity/time/", activitytime_urls),

    path("community/<int:pk>/", community_detail_urls),
    path("community/", community_urls),
    path("community/pic/", communitypic_urls),
    path("community/pic/<int:pk>/", communitypic_urls),

    path("history/<int:pk>/", history_detail_urls),
    path("history/", history_urls),
    path("historypic/", historypic_urls),

    path("analyse/", analyse_urls),

    # 种类
    path("type/", type_urls),
    path("type/<int:pk>/", type_detail_urls),

    # 学生逻辑
    path("stuactivity/sign/", sturegacivity_urls),
    path("stuactivity/sign/<int:pk>/", sturegacivity_detail_urls),

    path("stuactivity/", stuacivity_urls),
    path("stuactivity/<int:pk>/", stuacivity_detail_urls),

    path("stucommunity/", stucommunity_urls),
    path("stuhistory/", stuhistory_urls),

    path("stupass/download/", passstu_urls),

]
