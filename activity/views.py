from rest_framework import generics, permissions
from rest_framework.response import Response
from django.db.models import Sum
from datetime import datetime, timedelta
from .models import Activity
from .serializer import ActivitySerializer
from accounts.models import User


class ActivityListCreateView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Activity.objects.filter(user=self.request.user)
        date = self.request.query_params.get('date')
        if date:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
                queryset = queryset.filter(date=date_obj)
            except ValueError:
                pass
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only manage their own activities
        return Activity.objects.filter(user=self.request.user)


class CarbonFootprintView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        total_emission = Activity.objects.filter(user=request.user).aggregate(
            total=Sum('carbon_emission_kg')
        )['total'] or 0
        return Response({"total_carbon_kg": total_emission})


class LeaderboardView(generics.GenericAPIView):
    queryset = User.objects.all()

    def get(self, request):
        leaderboard = []
        for user in self.get_queryset():
            total = Activity.objects.filter(user=user).aggregate(
                total=Sum('carbon_emission_kg')
            )['total'] or 0
            leaderboard.append({"username": user.username, "total_emission": total})

        leaderboard.sort(key=lambda x: x['total_emission'])  # Less carbon = better
        return Response(leaderboard)

class ActivityByDateView(generics.ListAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        date_str = self.kwargs.get('date')
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Activity.objects.none()
        return Activity.objects.filter(user=user, date=date_obj)



class WeeklyActivityView(generics.ListAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        date_str = self.kwargs.get('date')
        try:
            end_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Activity.objects.none()

        weekday = end_date.weekday()  # Monday=0, Sunday=6
        days_since_sunday = (weekday + 1) % 7
        start_date = end_date - timedelta(days=days_since_sunday)
        return Activity.objects.filter(user=user, date__range=[start_date, end_date])


class MonthlyActivityView(generics.ListAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        date_str = self.kwargs.get('date')
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Activity.objects.none()

        first_day = date_obj.replace(day=1)
        if date_obj.month == 12:
            last_day = date_obj.replace(day=31)
        else:
            next_month = date_obj.replace(month=date_obj.month + 1, day=1)
            last_day = next_month - timedelta(days=1)
        return Activity.objects.filter(user=user, date__range=[first_day, last_day])
