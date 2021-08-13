from django.urls import path

from . import views

app_name = 'expenses'

urlpatterns = [
    path('transactions/', views.TransactionListView.as_view(), name = 'transactions'),
    path('create/', views.CreateTransactionView.as_view(), name='create'),
    path('<int:transaction_pk>/delete/', views.DeleteTransactionView.as_view(), name='delete'),
    path('<int:transaction_pk>/update/', views.UpdateTransactionView.as_view(), name='update'),
    path('categories/',views.CategoriesListView.as_view()  ,name='categories'),
    path('statistics/',views.StatisticsView.as_view() ,name='statics')
]