from flask import Blueprint, request, current_app
from model import Post, Usuario
from flask_jwt_extended import JWTManager

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, current_user

import form
bp = Blueprint('api', __name__, url_prefix='/api')

'''
GET - Obtener recurso
POST - Crear recurso
PUT - Modificar la totalidad de un recurso, es idempotente
PATCH - Modificar _parte_ de un recurso. No es idempotente
DELETE - Elimina un recurso

'''
# Inicializamos el Flask JWT
jwt = JWTManager()


@jwt.user_identity_loader
def obtener_sub_desde_usuario(usuario):
    return usuario.id

@jwt.user_lookup_loader
def obtener_usuario_desde_jwt(cabecera, cuerpo):
    return Usuario.obtener_usuario(int(cuerpo['sub']))



@bp.get('/')
def hola_mundo():
    return {"hola": "mundo"}

@bp.get('/post')
def retornar_posts():
    resultado = []
    for post in Post.obtener_posts():
        resultado.append(dict(
            usuario = post.usuario.usuario,
            fecha = post.fecha,
            cuerpo = post.cuerpo,
        ))

    return {
        'posts': resultado
    }

@bp.post('/post')
@jwt_required()
def crear_post():
    usuario = get_jwt_identity()

    try:
        cuerpo = request.json['cuerpo']
    except KeyError:
        return {
            'mensaje': "Falta el cuerpo"
        }, 400

    if not cuerpo:
        return {
            'mensaje': "Falta el cuerpo"
        }, 400

    Post.crear_post(
        usuario = usuario,
        cuerpo = cuerpo
    )

    return '', 201

@bp.delete('/post/<int:id>')
@jwt_required()
def borrar_post(id):
    usuario = current_user

    post = Post.obtener_post(id)

    if not post:
        return {"mensaje": "Post inexistente"}, 404

    if not usuario.es_administrador and post.usuario != usuario:
        return {"mensaje": "El post no pertence al usuario"}, 401

    post.borrar_post()

    return "", 201

@bp.get('/usuario/<usuario>')
def obtener_información_usuario(usuario):
    usuario = Usuario.obtener_usuario_desde_usuario(usuario)
    if not usuario:
        return {
            'mensaje': "Usuario inexistente"
        }, 404

    return {
        "usuario": dict(
            id = usuario.id,
            nombre = usuario.nombre,
            tiene_foto = usuario.tiene_foto,
        )
    }

@bp.post('/usuario')
def crear_usuario():
    frm = form.NuevoUsuarioApi(data = request.json)

    if frm.validate():
        Usuario.crear_usuario(**frm.data)
        return '', 204
    else:
        return {
            "mensajes": frm.errors
        }, 400



@bp.post('/sesión')
def iniciar_sesión():
    frm = form.IniciarSesiónApi(data = request.json)

    if not frm.validate():
        return {
            "mensajes": frm.errors
        }, 401

    usuario = frm.usuario_válido

    token = create_access_token(identity = usuario)

    return {
        'token': token
    }