# coding: utf-8

import docx
import csv
import smtplib
import subprocess
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(send_to, filename):
    send_from = 'pkcpweb@gmail.com'  # email do remetente
    password = 'Pkatherine1991'  # senha do email do remetente

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Subject'] = 'Certificados startup weekend women'
    text = '''
    Hola!!

    Gracias por haber participado del Startup Weekend Women Mendoza.
    Esperamos te haya sido de mucha ayuda para orientarte a la hora de comenzar con tu emprendimiento.

    Te enviamos adjunto el certificado de participación. Muchas gracias por ser parte de la comunidad SartUp Weekend!!

    --
    Florencia Rosas
    Co-organizer Startup Weekend

    '''
    msg.attach(MIMEText(text))

    filename = '{}.pdf/{}.pdf'.format(filename, filename)
    with open(filename, "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename(filename)
        )
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(filename)
        msg.attach(part)

    smtp = smtplib.SMTP('smtp.gmail.com:587')
    smtp.ehlo()
    smtp.starttls()
    smtp.login(send_from, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


def make_certificate(filename, name):
    doc = docx.Document(filename)
    for p in doc.paragraphs:
        if 'name' in p.text:
            inline = p.runs

            for i in range(len(inline)):
                if 'name' in inline[i].text:
                    inline[i].text = inline[i].text.replace('name', '')
                    inline[1].text = name + ' '
                    inline[1].bold = True
    doc.save('{}.docx'.format(name))

    try:
        subprocess.check_call([
            'unoconv', '-f',
            'pdf', '-o', '{}.pdf'.format(name), '-d', 'document',
            '{}.docx'.format(name)])
    except subprocess.CalledProcessError as e:
        print('CalledProcessError', e)


def certificate(filename):
    with open(filename, 'r') as csv_file:
        attendents = csv.reader(csv_file, delimiter=',')

        for row in attendents:
            make_certificate('certificado.docx', row[0])
            # send_mail(row[1], row[0])


if __name__ == '__main__':
    certificate('participantes.csv')
