from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('departments', views.DepartmentViewSet)
router.register('courses',     views.CourseViewSet)
router.register('students',    views.StudentViewSet)
router.register('enrollments', views.EnrollmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]