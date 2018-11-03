from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse, StreamingHttpResponse
from django.core.files.storage import  default_storage
from django.conf import settings
from django.core.files.base import  ContentFile
import os
from OnlineVideoStyleTransfer import transfer
import base64


# Create your views here.
def home(request):
    return render(request=request, template_name='index.html')

def index(request):
    if request.method == 'POST':

        file = request.FILES.get('file')

        if file != None:
            data = file.read()
            path = default_storage.save('content/content.mp4', ContentFile(data))
            path2 = default_storage.save('media/content.mp4', ContentFile(data))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)

            # 删除正在处理的文件 和已经处理好的文件这两个东西
            with open('nowPre.txt', 'w+') as tmpfile:
                tmpfile.write("")
            with open('nowProcessed.txt', 'w+') as tmpfile:
                tmpfile.write("")

            # 将视频转换为帧
            transfer.transferVideoToImage(contentvideo='content/content.mp4')

            imageFiles = os.listdir('generated/')

            for image in imageFiles:
                transfer.transfer(style_file=r'C:\Users\derfei\Desktop\专项设计最终版\onlinetransfer\OnlineVideoStyleTransfer\models\wave.ckpt-done', content_file='generated/'+image, output_file='generatedImage/' + image)
                nowProcessImage = 'generatedImage/' + image
                nowProcessedImage = 'generated/' + image
                writeNowPorcessImage(nowProcessImage, 'nowPre')
                writeNowPorcessImage(nowProcessedImage, 'nowProcessed')



            transfer.transferImageToVideo('generatedImage', outputVideoPath=os.path.join(settings.MEDIA_ROOT, "content_transfer.mp4"))
            transfer.transferImageToVideo('media\content_transfer.mp4')

            # 删除正在处理的文件 和已经处理好的文件这两个东西
            with open('nowPre.txt', 'w+') as tmpfile:
                tmpfile.write("")
            with open('nowProcessed.txt', 'w+') as tmpfile:
                tmpfile.write("")

            return HttpResponse("Done")
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def getPreImage(request):
    nowProcessImage = getNowProcessImage('nowPre')
    print("get the preImage" + nowProcessImage)
    nowProcessImage = nowProcessImage.replace("\n", "")
    if nowProcessImage != '':
        with open(nowProcessImage, 'rb') as f:
            image_data = f.read()
    else:
        with open('static/image_ware.png', 'rb') as f:
            image_data = f.read()
            return HttpResponse("data:image/png;base64," + base64.encodebytes(image_data).decode(),
                                content_type="image/png")

    return HttpResponse("data:image/jpg;base64,"+base64.encodebytes(image_data).decode(), content_type="image/jpg")

def getProcessedImage(request):
    nowProcessedImage = getNowProcessImage('nowProcessed')
    nowProcessedImage = nowProcessedImage.replace('\n', "")
    if nowProcessedImage != '':
        with open(nowProcessedImage, 'rb') as f:
            image_data = f.read()
    else:
        with open('static/image_ware.png', 'rb') as f:
            image_data = f.read()
            return HttpResponse("data:image/png;base64," + base64.encodebytes(image_data).decode(),
                                content_type="image/png")

    return  HttpResponse("data:image/jpg;base64,"+base64.encodebytes(image_data).decode(), content_type="image/jpg")

def getVideoPost(request):
    with open('static/video_ware.png', 'rb') as f:
        image_data = f.read()
    return HttpResponse("data:image/png;base64," + base64.encodebytes(image_data).decode(),
                                content_type="image/png")


def getNowProcessImage(file_name):
    with open(file_name + ".txt", 'r+') as file:
        alllines = file.readlines()
        if len(alllines) == 0:
            return ''
        else:
            return alllines[-1]
def writeNowPorcessImage(msg, file_name):
    with open(file_name + ".txt", 'a+') as file:
        file.writelines(msg + "\n")

def getProgress(request):
    imageFiles = os.listdir('generated/')
    datalistlen = len(imageFiles)

    datadonelen = 0
    with open('nowProcessed.txt', 'r+') as file:
        datadonelen = len(file.readlines())
    if datalistlen == 0:
        return HttpResponse('0')

    return HttpResponse(str((datadonelen/datalistlen)*100))
