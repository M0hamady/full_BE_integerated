
# views.py
# views.py
from rest_framework.response import Response
from rest_framework import generics
from .models import Category, EmployeeWebsite, Pic
from .serializers import EmployeeWebsiteSerializer, PicSerializer

class EmployeeWebsiteListCreateView(generics.ListCreateAPIView):
    queryset = EmployeeWebsite.objects.all()
    serializer_class = EmployeeWebsiteSerializer

class EmployeeWebsiteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmployeeWebsite.objects.all()
    serializer_class = EmployeeWebsiteSerializer

    def update(self, request, *args, **kwargs):
        partial = True  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class PicListAPIView(generics.ListAPIView):
    queryset = Pic.objects.all()
    serializer_class = PicSerializer

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from django.shortcuts import redirect
from django.shortcuts import render
from .forms import EmployeeForm, PicUploadForm
class ClientUuid(TemplateView):
    template_name = 'website/access_client.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uuid = kwargs['uuid']
        context['uuid'] = uuid
        return context


class PicUploadView(TemplateView):
    template_name = 'website/pic_upload.html'

    def get(self, request, *args, **kwargs):
        form = PicUploadForm()
        categories = Category.objects.all()
        return render(request, self.template_name, {'form': form,'categories': categories})

    def post(self, request, *args, **kwargs):
        form = PicUploadForm(request.POST, request.FILES)
        categories = Category.objects.all()
        print(request.FILES)
        if form.is_valid():
            pic = form.save()
            # Optionally, perform any additional processing or validation here
            return render(request, self.template_name, {'form': form, 'categories': categories, 'pic': pic})
        else:
            return render(request, self.template_name, {'form': form, 'categories': categories})
class EmployeeUploadView(TemplateView):
    template_name = 'website/employee.html'

    def get(self, request, *args, **kwargs):
        form = EmployeeForm()
        
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save()
            # Optionally, perform any additional processing or validation here
            return render(request, self.template_name, {'form': form, 'employee': employee})
        else:
            return render(request, self.template_name, {'form': form})