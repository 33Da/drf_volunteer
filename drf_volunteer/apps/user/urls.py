from . import views
from django.urls import path

# 用户操作
user_urls = views.UserViewset.as_view(
    {
    "get": "list",
    "post": "create",
    "put": "update",
    }
)

# 用户操作
password_urls = views.PasswordViewset.as_view()

# 管理员操作
admin_urls = views.AdminViewset.as_view({
    "get": "list",
    "post": "create",
    "put": "update",
})


admin_detail_urls = views.AdminViewset.as_view({
    "get":"retrieve",
    "delete": "destroy"
})

organ_urls = views.OrganViewset.as_view({
    "get": "list",
    "post": "create",
})


organ_detail_urls = views.OrganViewset.as_view({
    "get":"retrieve",
    "put":"update",
    "delete": "destroy"
})


urlpatterns = [
    # 用户逻辑
    path("user/", user_urls),
    path("user/password/", password_urls),

    path("admin/user/",admin_urls),
    path("admin/user/<int:pk>/",admin_detail_urls),

    path("organ/", organ_urls),
    path("organ/<int:pk>/", organ_detail_urls),

]
