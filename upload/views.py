# Create your views here.

from django.http import HttpResponse
from upload.forms import UploadFileForm
from upload.models import UploadFileModel



def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            model = form.save(commit=False)
            # test code
            model.devtype = '1'
            model.devhash = '2'
            model.deversion = '3'
            model.devip = '4'
            model.filename = model.filepath.name
            model.filemd5 = '6'
            model.filetype = '7'
            model.clientip = '8'
            print type(model.filepath)
            print dir(model.filepath)
            #test code

            model.save()
            return HttpResponse('success')
        else:
            return HttpResponse('form is not valid<br>' + str(form.errors))
    else:
        return HttpResponse("<form method='post' enctype='multipart/form-data'>\
                                <input name='path' type='text'>\
                                <input name='filemd5' type='text'>\
                                <input name='params' type='text'>\
                                <input name='lang' type='text'>\
                                <input name='filepath' type='file'>\
                                <input type='submit'>\
                            </form>")

    
def test(request):
    return HttpResponse('123321321')
