from django.contrib import admin
from django.urls import path
from website.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_view
from website.form import *




urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', about, name='about'),
    path('', home, name='home'),
    path('updateaddress/<int:pk>/',updateAddress.as_view(),name='updateAddress'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('address/',address,name='address'),
    path('contact/', contact, name='contact'),
    path('register/',  CustomerRegistrationView.as_view(), name='register'),
    path('login/',auth_view.LoginView.as_view(template_name='login.html',authentication_form=LoginForm),name='login'),
    path('categorytitle/<val>/', CategoryTitle.as_view(), name='categorytitle'), 
    path('productdetail/<int:pk>/', ProductDetail.as_view(), name='productdetail'), 
    path('category/<slug:val>/', CategoryView.as_view(), name='category'), 
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='passwordchange.html',form_class=MypasswordChangeForm,success_url='/passwordchangedone'),name='passwordchange'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'),name='passwordchangedone'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),
   
    path ('password-reset/', auth_view.PasswordResetView.as_view(template_name='password_reset.html',form_class=MyPasswordResetForm) , name='password_reset'),
    path( 'password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name= 'password_reset_done'),
    path( 'password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=MySetPasswordForm) , name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html') , name='password_reset_complete'),
   

    path('add-to-cart/',add_to_cart,name='add-to-cart'),
    path('cart/',show_cart,name='showcart'),

    path('pluscart/',plus_cart,name='pluscart'),
    path('minuscart/',minus_cart,name='minuscart'),
    path('removecart/',remove_cart,name='remove_cart'),
    path('checkout/',checkout.as_view(),name='checkout'),
    #path('paymentdone/',payment_done,name='payment_done'),
    path('pluswishlist/',plus_wishlist),
    path('minuswishlist/',minus_wishlist),
    ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )

