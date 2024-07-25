import os
from django.shortcuts import render, get_object_or_404, redirect

from document_management.models import Document
from document_management.forms import DocumentForm
from django.http import HttpResponse
from django.core.files.uploadedfile import SimpleUploadedFile
from .utils import convert_to_html


def document_list(request):
    documents = Document.objects.all().order_by('-created_at')
    return render(request, 'document_management/document_list.html', {'documents': documents})

def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    return render(request, 'document_management/document_detail.html', {'document': document})

def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded file
            file = request.FILES['file']
            
            # Read file content
            file_content = file.read().decode('utf-8')
            
            # Convert file content to HTML
            html_content = convert_to_html(file_content)
            
            # Create a new document instance
            document = form.save(commit=False)
            
            # Truncate the filename
            max_filename_length = 100
            file_name, file_extension = os.path.splitext(file.name)
            truncated_file_name = file_name[:max_filename_length - len(file_extension)] + file_extension
            
            # Save the original file and HTML content
            document.file.save(truncated_file_name, file)
            document.file_html = html_content  # Save HTML content directly
            document.save()
            
            return redirect('document_detail', pk=document.pk)
    else:
        form = DocumentForm()
    
    return render(request, 'document_management/document_form.html', {'form': form})

def document_update(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('document_list')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'document_management/document_form.html', {'form': form})





