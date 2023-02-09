from django.urls import path
from . import views as shopviews
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('complain/', shopviews.complain, name='complain'),
    path('review/', shopviews.review, name='review'),
    path('about/', shopviews.about_us, name='about_us'),
    # path('inquiry/', shopviews.inquiry, name='inquiry'),
    path('sellcar/', shopviews.car_request, name='request'),
    path('car/<int:id>', shopviews.cardetails, name='car'),
    # path('payment/', shopviews.payment, name='payment'),
    path('gallery/<int:cid>', shopviews.gallery, name='gallery'),
  
    # payment
    # path('order/<int:id>/',shopviews.car_order, name='car_order'),
    path('payment/car/<int:id>/',shopviews.car_order, name='payment'),
    path('order-success/',shopviews.order_success, name='order_success'),
    # path('payment/checkout/', shopviews.checkout, name='checkout'),
    # path('payment/charge/', shopviews.charge, name='charge'),
    # path('payment/success/', shopviews.success, name='success'),
    
    # account
    path('dashboard/', shopviews.dashboard, name='dashboard'),
    path('account/orders', shopviews.order, name='order'),
    path('accounts/login/', shopviews.user_login, name='login'),
    path('accounts/logout/', shopviews.user_logout, name='logout'),
    path('accounts/signup/', shopviews.user_signup, name='signup'),      
    path('accounts/changepass/', shopviews.changepass, name='changepass'),

    # reset password url
    path('accounts/password-reset/', auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('accounts/password-reset/done/', auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    

] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# add a flag for
# handling the 404 error
# handler404 = 'first.views.error_404_view'
