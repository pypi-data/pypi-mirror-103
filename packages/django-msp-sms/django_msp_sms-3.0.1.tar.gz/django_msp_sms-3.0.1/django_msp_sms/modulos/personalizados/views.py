#encoding:utf-8
from django.shortcuts import render,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
# user autentication
from .models import *
from .forms import *
from .core import *
from microsip_api.apps.sms.core import SMSMasivo
from django.conf import settings
#modo_pruebas = settings.MODO_SERVIDOR == 'PRUEBAS'


def get_num_enviados(respuestas):
    num_enviados = 0
    if type(respuestas) == list:
        num_enviados = 0
        for m in respuestas:
            if m['estatus'] == 'ok':
                num_enviados+=1        
    return num_enviados

@login_required(login_url='/login/')
def PorSeleccionView(request, template_name='django_msp_sms/personalizados/por_seleccion.html'):

    apikey=str(Registry.objects.get( nombre = 'SIC_SMS_ApiKey').get_value())
    modo_pruebas=Registry.objects.get(nombre='SIC_SMS_ModoPruebas').get_value() == 'S'
    clientes_con_telefono_invalido=[]
    mensaje_respuesta = ''
    estatus = ''
    multi=False
    num_enviados = 0
    form = SelectMultipleClients(
        request.POST or None)
    if form.is_valid():
        mensaje = form.cleaned_data['mensaje']
        clientes = form.cleaned_data['clientes']
        telfonos_clientes= TelefonosClientes(clientes=clientes)
        telefonos = telfonos_clientes.telefonos
        clientes_con_telefono_invalido = telfonos_clientes.clientes_con_telefono_invalido
        
        if None in clientes_con_telefono_invalido:
            clientes_con_telefono_invalido.remove(None)

        sms_masivo=SMSMasivo(apikey=apikey,pruebas=modo_pruebas)

        if (len(telefonos)>1):            
            telefono=",".join(telefonos)
            multi=True
            j = sms_masivo.multisend(mensaje=mensaje,telefono=telefono)
            mensaje_respuesta = j['respuestas']
            estatus = None
        elif len(telefonos)!= 0:
            telefono=telefonos[0]
            j = sms_masivo.send(mensaje=mensaje,telefono=telefono)
            mensaje_respuesta = j['mensaje']
            estatus = j['estatus']
        else:
            mensaje_respuesta='Ningun Telefono es Valido'

        num_enviados=get_num_enviados(mensaje_respuesta)
        
    c={'mensaje':mensaje_respuesta, 'form':form,'estatus':estatus,'multi':multi,'clientes_con_telefono_invalido':clientes_con_telefono_invalido, 'num_enviados':num_enviados,}

    return render(request, template_name,c)
    #return render_to_response( template_name, c , context_instance = RequestContext( request ) )

@login_required(login_url='/login/')
def TodosView( request, template_name = 'django_msp_sms/personalizados/todos.html' ):
    apikey=str(Registry.objects.get( nombre = 'SIC_SMS_ApiKey').get_value())
    num_enviados=0
    clientes_con_telefono_invalido=[]
    c={}
    multi=False
    form = SMSForm(request.POST or None)
    mensaje_respuesta = ''
    estatus = ''
    if form.is_valid():
        mensaje = form.cleaned_data['mensaje']
        telfonos_clientes=TelefonosClientes()
        telefonos = telfonos_clientes.telefonos
        clientes_con_telefono_invalido = telfonos_clientes.clientes_con_telefono_invalido
        if None in clientes_con_telefono_invalido:
            clientes_con_telefono_invalido.remove(None)
        sms_masivo=SMSMasivo(apikey=apikey,pruebas=modo_pruebas)
        creditos_antes =int(sms_masivo.credito()['credito'])

        if (len(telefonos)>1):            
            telefono=",".join(telefonos)
            multi=True
            j = sms_masivo.multisend(mensaje=mensaje,telefono=telefono)
            mensaje_respuesta = j['respuestas']
            estatus = None
        elif len(telefonos)!= 0:
            telefono=telefonos[0]
            j = sms_masivo.send(mensaje=mensaje,telefono=telefono)
            mensaje_respuesta = j['mensaje']
            estatus = j['estatus']

        else:
            mensaje_respuesta='Ningun Telefono es Valido'
        num_enviados=get_num_enviados(mensaje_respuesta) 
    c={'mensaje':mensaje_respuesta,'form':form,'estatus':estatus,'multi':multi,'clientes_con_telefono_invalido':clientes_con_telefono_invalido,'num_enviados':num_enviados, }

    return render(request, template_name,c)
    #return render_to_response( template_name, c, context_instance = RequestContext( request ) )


@login_required(login_url='/login/')
def ZonaView(request, template_name='django_msp_sms/personalizados/zona.html'):
    apikey = str(Registry.objects.get(nombre='SIC_SMS_ApiKey').get_value())
    sms_masivo = None
    num_enviados = 0
    creditos_antes = 0
    creditos_despues = 0
    clientes_con_telefono_invalido = []
    c = {}
    multi = False
    form = ZonaForm(request.POST or None)
    mensaje_respuesta = ''
    estatus = ''
    if form.is_valid():

        mensaje = form.cleaned_data['mensaje']
        zona = form.cleaned_data['zona']

        telfonos_clientes = TelefonosClientes(zona=zona)
        telefonos = telfonos_clientes.telefonos
        clientes_con_telefono_invalido = telfonos_clientes.clientes_con_telefono_invalido

        if None in clientes_con_telefono_invalido:
            clientes_con_telefono_invalido.remove(None)

        sms_masivo = SMSMasivo(apikey=apikey, pruebas=modo_pruebas)

        if (len(telefonos) > 1):
            telefono = ",".join(telefonos)
            multi = True
            j = sms_masivo.multisend(mensaje=mensaje, telefono=telefono)
            mensaje_respuesta = j['respuestas']
            estatus = None
        elif len(telefonos) != 0:
            telefono = telefonos[0]
            j = sms_masivo.send(mensaje=mensaje, telefono=telefono)
            mensaje_respuesta = j['mensaje']
            estatus = j['estatus']
        else:
            mensaje_respuesta = 'Ningun Telefono es Valido'
        num_enviados = get_num_enviados(mensaje_respuesta)

    c = {'mensaje': mensaje_respuesta, 'form': form, 'estatus': estatus, 'multi': multi, 'clientes_con_telefono_invalido': clientes_con_telefono_invalido, 'num_enviados': num_enviados}
    return render(request, template_name,c)
    #return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def archivoView(request, template_name='django_msp_sms/personalizados.html'):
    apikey = str(Registry.objects.get(nombre='SIC_SMS_ApiKey').get_value())
    c = {}
    multi = False
    form = SMSForm(request.POST or None)
    mensaje_respuesta = ''
    estatus = ''
    if form.is_valid():
        mensaje = form.cleaned_data['mensaje']
        mensaje = mensaje.encode('ascii', 'replace')
        telefono = form.cleaned_data['telefono']
        sms_masivo = SMSMasivo(apikey=apikey, pruebas=modo_pruebas)

        if (len(telefono.split(',')) > 1):
            multi = True
            j = sms_masivo.multisend(mensaje=mensaje, telefono=telefono)
            mensaje_respuesta = j['respuestas']
            estatus = None
        else:
            j = sms_masivo.send(mensaje=mensaje, telefono=telefono)
            mensaje_respuesta = j['mensaje']
            estatus = j['estatus']

    c = {'mensaje': mensaje_respuesta, 'form': form, 'estatus': estatus, 'multi': multi, }
    return render(request, template_name,c)
    #return render_to_response(template_name, c, context_instance=RequestContext(request))
