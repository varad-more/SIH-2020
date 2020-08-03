from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import portrait
from reportlab.platypus import Image

import csv

data_file = 'Corporate_Actions.csv'

def import_data(data_file):
    ca_data = csv.reader(open(data_file,"rt"))
    for row in ca_data:

        # security_id = row[0]
        # isin = row[1]
        # security_code = row[2]
        # trading_symbol = row[]
        # security_name = row[]
        # status = row[]
        # security_group = row[]
        # face_value = row[]
        # industry = row[]
        # instrument = row[]
        # nse_listed = row[]
        # bse_listed = row[]
        # trading_location = row[]
        Security_Code = row[0]
        Security_Name = row[1]
        Company_Name = row[2]
        Ex_Date = row[3]
        Purpose = row[4]
        Record_Date = row[5]
        Start_Date_1 = row[6]
        End_Date_1	 = row[7]
        Start_Date_2 = row[8]
        End_Date_2 = row[9]
        Actual_Payment_Date = row[10]
        pdf_file_name = Company_Name + '_' + Security_Code + '.pdf'
        generate_certificate(Security_Code,Security_Name,Company_Name,Ex_Date,Purpose,Record_Date,Start_Date_1,End_Date_1,Start_Date_2,End_Date_2,Actual_Payment_Date,pdf_file_name)

def generate_certificate(Security_Code,Security_Name,Company_Name,Ex_Date,Purpose,Record_Date,Start_Date_1,End_Date_1,Start_Date_2,End_Date_2,Actual_Payment_Date,pdf_file_name):

        
    c = canvas.Canvas(pdf_file_name, pagesize = portrait(letter))

    c.setFont('Helvetica-Bold', 35, leading = None)
    c.drawCentredString(300,750,"Corporate Action Summary")
    c.setFont('Helvetica', 20, leading = None)
    c.drawString(20, 680,"Security Code: ")
    c.drawString(300, 680,Security_Code)
    # c.setFont('Helvetica', 30, leading = None)
    # c.drawString(100, 450,"Security_Name Code: ",Security_Name)
    # c.setFont('Helvetica', 30, leading = None)
    # c.drawString(100, 400,"Company_Name: ",Company_Name)
    # c.setFont('Helvetica', 30, leading = None)
    # c.drawString(100, 350,"Ex_Date: ",Ex_Date)
    # c.setFont('Helvetica', 30, leading = None)
    # c.drawString(100, 300,"Purpose: ",Purpose)
    # c.setFont('Helvetica', 30, leading = None)
    # c.drawString(100, 250,"Record_Date: ",Record_Date)
    # c.setFont('Helvetica', 30, leading = None)
    # c.drawString(100, 200,"Start_Date: ",Start_Date)
    # c.setFont('Helvetica', 30, leading = None)
    # c.drawString(100, 150,"End_Date: ",End_Date)
    # c.setFont('Helvetica', 30, leading = None)
    # c.drawString(100, 100,"Actual_Payment: ",Actual_Payment_Date)
    logo = 'sih logo.png'
    c.drawImage(logo,300,50, width=None, height=None)
    c.showPage()
    c.save()
    print('writing...')
import_data(data_file)