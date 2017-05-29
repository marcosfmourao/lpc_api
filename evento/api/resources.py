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
    def obj_create(self, bundle, **kwargs):
        x = bundle.data['pessoa'].split("/")
        y = bundle.data['evento'].split("/")
        print(x[4])
        print(y[4])
        if not(Inscricoes.objects.filter(pessoa = x[4]) and Inscricoes.objects.filter(evento = y[4])):
            e = bundle.data['evento'].split("/")
            t = bundle.data['tipo'].split("/")

            inscricao = Inscricoes()

            inscricao.pessoa = PessoaFisica.objects.get(pk = int(x[4]) )
            inscricao.evento = Evento.objects.get(pk = int(e[4]) )
            inscricao.tipoInscricao = TipoInscricao.objects.get(pk = int(t[4]) )

            inscricao.dataEHoraDaInscricao = bundle.data["dataEHoraDaInscricao"]
            inscricao.save()
            bundle.obj = inscricao
            return bundle
        else:
            raise Unauthorized("Pessoa ja cadastrada no evento!")

    pessoa = fields.ToOneField(PessoaFisicaResource, 'pessoa')
    evento = fields.ToOneField(EventoResource, 'evento')
    tipo = fields.ToOneField(TipoInscricaoResource, 'tipoInscricao')
    class Meta:
        queryset = Inscricoes.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = {
            "descricao": ('exact', 'startswith')
        }




class EventoCientificoResource(ModelResource):
    class Meta:
        queryset = EventoCientifico.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = {
            "issn": ('exact', 'startswith',)
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
    eventoCientifico = fields.ToOneField(EventoCientificoResource, 'evento')
    class Meta:
        queryset = ArtigoCientifico.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = {
            "titulo": ('exact', 'startswith',)
        }

class ArtigoAutorResource(ModelResource):
        artigoCientifico= fields.ToOneField(ArtigoCientificoResource, 'artigoCientifico')
        autor = fields.ToOneField(PessoaFisicaResource, 'autor')

        class Meta:
            queryset = ArtigoAutor.objects.all()
            allowed_methods = ['get', 'post', 'delete', 'put']
            authorization = Authorization()
