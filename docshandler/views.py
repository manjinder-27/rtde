from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Document

@login_required
def createDoc(request):
    doc = Document()
    doc.name = request.POST['filename']
    doc.content = ''
    doc.owner = request.user
    doc.save()
    docID = doc.uniqID
    return redirect('../editor/'+str(docID))


@login_required
def openEditor(request,docID):
    doc_res = Document.objects.filter(uniqID=docID)
    if doc_res.exists():
        doc = doc_res[0]
        context = {
            'filename':doc.name,
            'content':doc.content,
            'room_name':docID,
            'username':request.user.username,
            'close_btn_status':'disabled',
            'del_btn_display':'none'
        }
        if doc.owner == request.user:
            context['close_btn_status'] = ''
            context['del_btn_display'] = 'inline-block'
        return render(request,'editor.html',context=context)
    else:
        return render(request,'errorPage.html')


@login_required
def connectView(request):
    docID = request.POST['docID']
    doc = Document.objects.filter(uniqID=docID)
    return redirect('../editor/'+docID)

@login_required
def downloadFile(request,docID):
    doc_res = Document.objects.filter(uniqID=docID)
    if doc_res.exists():
        data = doc_res[0].content
        response = HttpResponse(data, content_type="text/plain")
        response["Content-Disposition"] = 'attachment; filename="' + doc_res[0].name + '"'
        return response
    else:
        return render(request,'errorPage.html')