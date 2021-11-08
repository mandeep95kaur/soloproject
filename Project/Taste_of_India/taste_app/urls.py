from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from .forms import MyPasswordChangedForm

urlpatterns = [
    path('', views.ProductView.as_view(), name='home'),
    path('product-detail/<int:id>', views.ProductDetailView.as_view(), name='product-detail'),
    path('cart/',views.show_cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add-to-cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='passwordchange.html', 
    form_class= MyPasswordChangedForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html',
    authentication_form=LoginForm), name='login'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('reviews/',views.review , name='reviews'),
    path('add_review/',views.create_review),
    path('reviews/<int:review_id>/like',views.like_review),
    path('reviews/<int:review_id>/unlike',views.unlike_review),
    path('reviews/<int:review_id>/delete',views.delete_review),
    path('logout/', auth_views.LogoutView.as_view(next_page='/') , name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)