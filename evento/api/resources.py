from tastypie.resources import ModelResource
from tastypie import fields, utils
from evento.models import *
from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


class TipoInscricaoResource(ModelResource):
    def obj_create(self, bundle, **kwargs):
        print (bundle.data)
        tipo = TipoInscricao()
        tipo.descricao = bundle.data['descricao'].upper()
        if TipoInscricao.objects.filter(descricao = tipo.descricao).exists():
            print ("Nome já existe")
            raise Unauthorized ('Já existe tipo com este nome')
        else:
            tipo.save()
            bundle.obj = tipo
        return bundle

    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized ('Não pode apagar uma lista!')






    class Meta:
        queryset = TipoInscricao.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = {
            "descricao": ('exact', 'startswith',)
        }


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        resource_name = 'user'
        excludes = ['password', 'is_active']


class PessoaFisicaResource(ModelResource):
    class Meta:
        queryset = PessoaFisica.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = {
            "cpf": ('exact', 'startswith',)
        }

class EventoResource(ModelResource):
    realizador = fields.ToOneField(PessoaFisicaResource, 'realizador')
    class Meta:
        queryset = Evento.objects.all()
        resource_name = 'evento'
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = {
            "nome": ('exact', 'startswith',)
        }

class InscricaoResource(ModelResource):


    pessoa = fields.ToOneField(PessoaFisicaResource, 'pessoa')
    evento = fields.ToOneField(EventoResource, 'evento')
    tipoInscricao = fields.ToOneField(TipoInscricaoResource, 'tipoInscricao')

    #tipo = TipoInscricao()
    #tipo.descricao = bundle.data['descricao'].upper()
    #if TipoInscricao.objects.filter(descricao = tipo.descricao).exists():
        #print ("Nome já existe")
        #raise Unauthorized ('Já existe tipo com este nome')
    #def obj_create(self, bundle, **kwargs):
    #    insc = Inscricoes()
    #    insc.PessoaFisica = bundle.data['pessoa']
    #    insc.Evento = bundle.data['evento']
    #    if Inscricoes.objects.filter(evento = insc.evento) and Inscricoes.objects.filter(evento = insc.pessoa):
    #            def obj_create(self, bundle, **kwargs):
    #                raise Unauthorized ('Não pode inserir a mesma pessoa + de uma vez!')





    class Meta:
        queryset = Inscricoes.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()



class EventoCientificoResource(ModelResource):
    realizador = fields.ToOneField(PessoaFisicaResource, 'realizador')
    class Meta:
        queryset = EventoCientifico.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = {  "issn": ('exact', 'startswith',)
        }


class PessoaResource(ModelResource):
    class Meta:
        queryset = Pessoa.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = { "nome": ('exact', 'startswith',)
        }



class PessoaJuridicaResource(ModelResource):
    class Meta:
        queryset = PessoaJuridica.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = { "razaoSocial": ('exact', 'startswith',)
        }


class AutorResource(ModelResource):
    class Meta:
        queryset = Autor.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = {
            "curriculo": ('exact', 'startswith',)
        }


class ArtigoCientificoResource(ModelResource):
    evento = fields.ToOneField(EventoCientificoResource, 'evento')
    class Meta:
        queryset = ArtigoCientifico.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = {
            "titulo": ('exact', 'startswith',)
        }

class ArtigoAutorResource(ModelResource):
    class Meta:
        artigoCientifico= fields.ToOneField(ArtigoCientificoResource, 'artigoCientifico')
        autor = fields.ToOneField(PessoaFisicaResource, 'autor')

        class Meta:
            queryset = ArtigoAutor.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
