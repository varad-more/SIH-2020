from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required,permission_required
from dashboard.models import file_download,corp_action_data,articles,company, dashboard,errors, historic_data, links, pages, securities,links 
import mysql.connector 


import io
import ast
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph

# Create your views here.

@login_required
@permission_required ('corp_action_data.view_user')
def index (request):
    data = corp_action_data.objects.all()
    data_1 = corp_action_data.objects.filter(ca_type="dividends")
    data_2 = corp_action_data.objects.filter(ca_type="board_meeting")
    data_3 = corp_action_data.objects.filter(ca_type="agm_egm")
    data_4 = corp_action_data.objects.filter(ca_type="bonus")
    data_5 = corp_action_data.objects.filter(ca_type="book closures")
    data_6 = corp_action_data.objects.filter(ca_type="rights")
    data_7 = corp_action_data.objects.filter(ca_type="splits")

    content = {
        'data':data_1
    }

    return render (request , 'index.html',content)

@login_required
def report(request):
    #future expected page
    data = articles.objects.filter(news_checked__gt = 0)
    print (type (data))
    content = {
        'data':data
    }
    return render (request, 'report.html',content)

@login_required
def dash_web(request):
    count = []
    ca = []

    data = corp_action_data.objects.all()
    for d in data:
         
     
    content = {
        'ca_count':count,
        'data' : data
    }

    return render(request,'dashboard.html',content)

@login_required
def rep_generatoion(request):
    data = corp_action_data.objects.all()[:100]
    content = {
        'data':data
    }
    return render (request, 'gen.html', content) 


@login_required
def sec_master(request):
    data = corp_action_data.objects.all()[:100]
    content = {
        'data':data
    }
    return render (request, 'secmast.html', content) 



def pdf_downloader(request):
    Company_Name = request.GET['Company_Name']
    date_start = request.GET['date_start']
    date_end = request.GET['date_end']
    print (Company_Name)
    
    data_1 = corp_action_data.objects.get(company_name=Company_Name)    
    content = {'data':data_1}
    print (data_1.company_name, data_1.ca_type, data_1.data)

    from reportlab.lib.styles import getSampleStyleSheet
    sample_style_sheet = getSampleStyleSheet()
    #PDF Generation

    import matplotlib.pyplot as plt
    data = {'apple': 10, 'orange': 15, 'lemon': 5, 'lime': 20}
    names = list(data.keys())
    values = list(data.values())

    fig, axs = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
    axs[0].bar(names, values)
    axs[1].scatter(names, values)
    axs[2].plot(names, values)
    fig.suptitle('Categorical Plotting')
    plt.savefig('1.png')
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    # data_1 = str (data_1)
    p.drawString(100, 100, "PYTHANOS"+ data_1.ca_type)
    # p.drawString("Test")
    # p.drawInlineImage('1.png',0,0, width=None,height=None)
    #Paragraph("A title", sample_style_sheet['Heading1'])
    # paragraph_2 = Paragraph("Some normal body text", sample_style_sheet['BodyText'])
    
    p.showPage()
    p.save()
    buffer.seek(0)

    '''
    from io import BytesIO
    from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import mm, inch
    PAGESIZE = (140 * mm, 216 * mm)  
    BASE_MARGIN = 5 * mm
    class PdfCreator:    
        def add_page_number(self, canvas, doc):
            canvas.saveState()
            canvas.setFont('Times-Roman', 10)
            page_number_text = "%d" % (doc.page)
            canvas.drawCentredString(
                0.75 * inch,
                0.75 * inch,
                page_number_text
            )
            canvas.restoreState()
        
        def get_body_style(self):
            sample_style_sheet = getSampleStyleSheet()
            body_style = sample_style_sheet['BodyText']
            body_style.fontSize = 18
            return body_style
        
        def build_pdf(self):
            pdf_buffer = BytesIO()
            my_doc = SimpleDocTemplate(
                pdf_buffer,
                pagesize=PAGESIZE,
                topMargin=BASE_MARGIN,
                leftMargin=BASE_MARGIN,
                rightMargin=BASE_MARGIN,
                bottomMargin=BASE_MARGIN)

            body_style = self.get_body_style()        
            
            flowables = [
            Paragraph("First paragraph", body_style),
            Paragraph("Second paragraph", body_style)]        
            
            my_doc.build(
            flowables,
            onFirstPage=self.add_page_number,
            onLaterPages=self.add_page_number,)
            pdf_value = pdf_buffer.getvalue()
            pdf_buffer.close()
    '''
    print("executed")
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
    # pass





def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print("form is valid")
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render (request,'register.html', {'form':form})
