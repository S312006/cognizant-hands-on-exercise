from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('departments', views.DepartmentViewSet)
router.register('courses', views.CourseViewSet)
router.register('students', views.StudentViewSet)
router.register('enrollments', views.EnrollmentViewSet)

urlpatterns = [
    # Hands-On 3, Task 1 - manual APIView endpoints (for learning)
    path('courses-manual/', views.CourseListView.as_view(), name='course-list-manual'),
    path('courses-manual/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail-manual'),

    # Hands-On 3, Task 2 - ViewSet + Router endpoints (auto-generated)
    path('', include(router.urls)),
]