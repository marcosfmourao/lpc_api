from tastypie.resources import ModelResource
from tastypie import fields, utils
from evento.models import *
from django.contrib.auth.models import User
from tastypie.authorization import Authorization


class TipoInscricaoResource(ModelResource):
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
