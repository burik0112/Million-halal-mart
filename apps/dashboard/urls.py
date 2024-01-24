from django.urls import path
from .product import (
    PhoneListView,
    PhoneCreateView,
    TicketCreateView,
    TicketListView,
    GoodListView,
    GoodCreateView,
    PhoneCategoryCreateView,
    TicketCategoryCreateView,
    PhoneEditDeleteView,
    PhoneDeleteView,
    GoodCategoryCreateView,
    TicketDeleteView,
    TicketEditDeleteView,
    GoodEditDeleteView,
    GoodDeleteView,
    GoodMainCategoryCreateView,
    CategoryCreateView,
    CategoryListView,
    CategoryEditView,
    CategoryDeleteView,
    SubCategoryCreateView,
    SubCategoryListView,
    SubCategoryEditView,
    SubCategoryDeleteView
)

from .users import (UserListView, UserOrdersView,
                    UserOrderDetailView, OrdersListView, BlockActivateUserView, update_order_status, login)
from .main import (dashboard, InformationView,BonusEditView,
                   InformationEditView, ServiceView, ServiceEditView, BannerView, BannerActionView, NewsCreateView, NewsListView, NewsEditView, OrdersView)
from .users import (
    UserListView,
    UserOrdersView,
    UserOrderDetailView,
    OrdersListView,
    BlockActivateUserView,
)
from .bot import index
from django.contrib.auth.decorators import login_required
from .information import (
    edit_reminder,
    edit_agreement,
    edit_shipment,
    edit_privacy,
    edit_aboutus,
    edit_support,
    edit_payment,
    SocialMediaListView,
    SocialMediaEditView,
)

urlpatterns = [
    path("", login_required(dashboard), name="dashboard"),
    path("product/category/create/", login_required(CategoryCreateView.as_view()), name='category-create'),
    path("product/category/list/", login_required(CategoryListView.as_view()), name='category-list'),
    path('product/category/edit/<int:pk>/', login_required(CategoryEditView.as_view()), name='category-edit'),
    path('product/category/<int:pk>/detelet', login_required(CategoryDeleteView.as_view()), name='category-delete'),
    path("product/subcategory/create/", login_required(SubCategoryCreateView.as_view()), name='subcategory-create'),
    path("product/subcategory/list/", login_required(SubCategoryListView.as_view()), name='subcategory-list'),
    path('product/subcategory/edit/<int:pk>/', login_required(SubCategoryEditView.as_view()), name='subcategory-edit'),
    path('product/subcategory/<int:pk>/detelet', login_required(SubCategoryDeleteView.as_view()), name='subcategory-delete'),

    path("product/create-phone/", login_required(PhoneCreateView.as_view()), name="create_phone"),
    path(
        "product/phone-category/",
        login_required(PhoneCategoryCreateView.as_view()),
        name="phone_category",
    ),
    path("product/phones/", login_required(PhoneListView.as_view()), name="phone_list"),
    path(
        "product/phones/edit-delete/<int:pk>/",
        login_required(PhoneEditDeleteView.as_view()),
        name="edit_delete_phone",
    ),
    path(
        "product/phone/<int:pk>/delete/", login_required(PhoneDeleteView.as_view()), name="delete_phone"
    ),
    path("product/ticket-create/", login_required(TicketCreateView.as_view()), name="ticket_create"),
    path(
        "product/ticket-category/",
        login_required(TicketCategoryCreateView.as_view()),
        name="ticket_category",
    ),
    path("product/tickets/", login_required(TicketListView.as_view()), name="ticket-list"),
    path(
        "product/ticket/edit-delete/<int:pk>/",
        login_required(TicketEditDeleteView.as_view()),
        name="edit_delete_ticket",
    ),
    path(
        "product/ticket/<int:pk>/delete/",
        login_required(TicketDeleteView.as_view()),
        name="delete_ticket",
    ),
    path("product/good-create/", login_required(GoodCreateView.as_view()), name="good_create"),
    path(
        "product/good-category/",
        login_required(GoodMainCategoryCreateView.as_view()),
        name="good_category",
    ),
    path(
        "product/good-subcategory/",
        login_required(GoodCategoryCreateView.as_view()),
        name="good_subcategory",
    ),
    path("product/goods/", login_required(GoodListView.as_view()), name="good-list"),
    path("product/good/edit-delete/<int:pk>/",
         login_required(GoodEditDeleteView.as_view()), name='edit-delete-good'),
    path('product/good/<int:pk>/delete/',
         login_required(GoodDeleteView.as_view()), name='delete_good'),


    path("product/news/", login_required(NewsListView.as_view()), name="news-list"),
    path("product/news-create/", login_required(NewsCreateView.as_view()), name="news-create"),
    # path('product/news/edit/<int:pk>/',
    #      NewsEditView.as_view()), name='edit_delete_news'),

    path("users/", login_required(UserListView.as_view()), name="users-list"),
    path("users/<int:pk>/order", login_required(UserOrdersView.as_view()), name="user-orders-list"),
    path("users/order-detail/<int:pk>/", login_required(UserOrderDetailView.as_view()), name="user-order-detail"),
    path('block_activate_user/<int:pk>/', login_required(BlockActivateUserView.as_view()), name='block_activate_user'),
    
    path("orders/", login_required(OrdersListView.as_view()), name="all-orders-list"),

    path("other/news/", login_required(NewsListView.as_view()), name="news-list"),
    path("other/news-create/", login_required(NewsCreateView.as_view()), name="news-create"),
    path('other/news/edit/<int:pk>/',
         login_required(NewsEditView.as_view()), name='edit_delete_news'),
    path('other/info/list/', login_required(InformationView.as_view()), name='info-list'),
    path('other/info/edit/<int:pk>/',
         login_required(InformationEditView.as_view()), name='edit_info'),
    path('other/service/list', login_required(ServiceView.as_view()), name='service-list'),
    path('other/service/edit/<int:pk>/',
         login_required(ServiceEditView.as_view()), name='edit_service'),
    path('other/banners/list/', login_required(BannerView.as_view()), name='banner-list'),
    path('other/banner/action/<int:pk>/',
         login_required(BannerActionView.as_view()), name='banner-action'),
    path("orders/<int:pk>/", login_required(OrdersView.as_view()), name="orders-list"),
    path('update-order-status/<int:pk>/',
         login_required(update_order_status), name='update-order-status'),

    path('bot/', index, name='bot'),
    # info
    path("edit-reminder/<int:pk>/", login_required(edit_reminder), name="edit_reminder"),
    path("edit-agreement/<int:pk>/", login_required(edit_agreement), name="edit_agreement"),
    path("edit-shipment/<int:pk>/", login_required(edit_shipment), name="edit_shipment"),
    path("edit-privacy/<int:pk>/", login_required(edit_privacy), name="edit_privacy"),
    path("edit-about_us/<int:pk>/", login_required(edit_aboutus), name="edit_aboutus"),
    path("edit-support/<int:pk>/", login_required(edit_support), name="edit_support"),
    path("edit-payment/<int:pk>/", login_required(edit_payment), name="edit_payment"),
    path("bonus-edit/<int:pk>/", login_required(BonusEditView.as_view()), name="edit_bonus"),
    path("socialmedia/", login_required(SocialMediaListView.as_view()), name="socialmedia"),
    path("socialmedia-edit/<int:pk>/", login_required(SocialMediaEditView.as_view()), name="edit_media"),


    
]
