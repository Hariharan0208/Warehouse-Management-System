from . import views
from django.urls import path

urlpatterns=[
    path('',views.Home_Page,name='Home_Page'),

    path('Login_Page',views.Login_Page,name='Login_Page'),
    path('LoginPage_Backend',views.LoginPage_Backend,name='LoginPage_Backend'),

    path('Sign_Page',views.Sign_Page,name='Sign_Page'),
    path('SignPage_Backend',views.SignPage_Backend,name='SignPage_Backend'),


    path('Admin_Home',views.Admin_Home,name='Admin_Home'),
    path('AdminPermission_Allow/<int:pk>',views.AdminPermission_Allow,name='AdminPermission_Allow'),
    path('AdminPermission_Denied/<int:pk>',views.AdminPermission_Denied,name='AdminPermission_Denied'),
    path('RemoveUser_Backend/<int:pk>',views.RemoveUser_Backend,name='RemoveUser_Backend'),
    path('UserList_Page',views.UserList_Page,name='UserList_Page'),
    path(' UserPermission_Page',views.UserPermission_Page,name=' UserPermission_Page'),
    
    path('AddCategory_Page',views.AddCategory_Page,name='AddCategory_Page'),
    path('AddCategoryPage_Backend',views.AddCategoryPage_Backend,name='AddCategoryPage_Backend'),

    path('CategoryList_Page',views.CategoryList_Page,name='CategoryList_Page'),
    path('Delete_CategoryItem/<int:pk>',views.Delete_CategoryItem,name='Delete_CategoryItem'),

    path('AddProduct_Page',views.AddProduct_Page,name='AddProduct_Page'),
    path('AddProductPage_Backend',views.AddProductPage_Backend,name='AddProductPage_Backend'),

    path('ProductList_Page',views.ProductList_Page,name='ProductList_Page'),
    path('EditProduct_Page/<int:pk>',views.EditProduct_Page,name='EditProduct_Page'),
    path('EditProductPage_Backend/<int:pk>',views.EditProductPage_Backend,name='EditProductPage_Backend'),
    path('Delete_ProductItem/<int:pk>',views.Delete_ProductItem,name='Delete_ProductItem'),
    path('AdminOrder_Page',views.AdminOrder_Page,name='AdminOrder_Page'),
    path('AdminOrderPage_Backend/<int:pk>',views.AdminOrderPage_Backend,name='AdminOrderPage_Backend'),

    path('UserHome_Page',views.UserHome_Page,name='UserHome_Page'),
    path("AddToCart_Page",views.AddToCart_Page,name="AddToCart_Page"),
    path("add_to_cart/<int:pk>",views.add_to_cart,name="add_to_cart"),
    path("remove_cart/<int:pk>",views.remove_cart,name="remove_cart"),
    path("Increase_quantity/<int:id>",views.Increase_quantity,name="Increase_quantity"),
    path("Decrease_quantity/<int:id>",views.Decrease_quantity,name="Decrease_quantity"),
    path("Buy_now_page/<int:pk>",views.Buy_now_page,name="Buy_now_page"),
    path("OrderTracking_Page",views.OrderTracking_Page,name='OrderTracking_Page'),
    path("BuyNowPage_Backend/<int:pk>",views.BuyNowPage_Backend,name='BuyNowPage_Backend'),
    path("UserProfile",views.UserProfile,name='UserProfile'),
    path("edit_profile/<int:pk>",views.edit_profile,name='edit_profile'),
    path("OrderSearch/<int:pk>",views.OrderSearch,name='OrderSearch'),
    path("Agentedit_profile/<int:pk>",views.Agentedit_profile,name='Agentedit_profile'),
    path('update_userprofile/<int:pk>',views.update_userprofile,name='update_userprofile'),
    path('ChangePassword',views.ChangePassword,name='ChangePassword'),

    path('AgentHome_Page',views.AgentHome_Page,name='AgentHome_Page'),
    path('AgentProfile',views.AgentProfile,name='AgentProfile'),
    path('ShipType_Page',views.ShipType_Page,name='ShipType_Page'),
    path("ShipType_Backend",views.ShipType_Backend,name='ShipType_Backend'),
    path('ShipTypeList_Page',views.ShipTypeList_Page,name='ShipTypeList_Page'),
    path(' Delete_ShipType/<int:pk>',views.Delete_ShipType,name='Delete_ShipType'),
    path('Delivery_Update/<int:pk>',views.Delivery_Update,name='Delivery_Update'),
    path('DeliverUpdate_Backend/<int:pk>',views.DeliverUpdate_Backend,name='DeliverUpdate_Backend'),
    path('DeliveryCondition/<int:pk>',views.DeliveryCondition,name='DeliveryCondition'),
    path("OrderList",views.OrderList,name='OrderList'),
    path('search_product',views.search_product,name='search_product'),
    path('LocationUpdate_Page/<int:pk>',views.LocationUpdate_Page,name='LocationUpdate_Page'),
    path('LocationUpdate_Back/<int:pk>',views.LocationUpdate_Back,name='LocationUpdate_Back'),
    path('Admin_OrderStatus/<int:pk>',views.Admin_OrderStatus,name='Admin_OrderStatus'),
]