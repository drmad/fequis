from flask import Blueprint, render_template, request, redirect, flash, url_for, session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from init import app, login_manager

from model import db, Usuario, Post
from form import NuevoUsuario, IniciarSesión, EditarUsuario

import datetime

bp = Blueprint('principal', __name__)


@login_manager.user_loader
def obtener_usuario(id):
    return db.session.get(Usuario, int(id))

@bp.route('/', methods=['GET', 'POST'])
def página_principal():
    if request.method == 'POST':
        posts = Post.crear_post(
            usuario = current_user,
            cuerpo = request.form['cuerpo'],
        )
        return redirect(request.referrer)

    posts = Post.obtener_posts()

    return render_template('mostrar_posts.html', posts = posts)


@bp.route('/nuevo-usuario', methods=['GET', 'POST'])
def nuevo_usuario():
    frm = NuevoUsuario()
    if request.method == 'POST':
        if frm.validate():
            Usuario.crear_usuario(
                nombre = frm.nombre.data,
                usuario = frm.usuario.data,
                correo_electrónico = frm.correo_electrónico.data,
                contraseña = frm.contraseña.data
            )

            # ph = PasswordHasher()
            # db.session.add(
            #     Usuario(
            #         nombre = frm.nombre.data,
            #         usuario = frm.usuario.data,
            #         correo_electrónico = frm.correo_electrónico.data,
            #         contraseña = ph.hash(frm.contraseña.data)
            #     )
            # )
            # db.session.commit()



            flash("Usuario creado correctamente")

            return redirect(url_for('principal.página_principal'))
        else:
            flash("Hubo errores en el formulario")



    return render_template('nuevo-usuario.html', frm = frm)

@bp.route('/iniciar-sesión', methods=['GET', 'POST'])
def iniciar_sesión():
    frm = IniciarSesión()

    if request.method == 'POST':
        if frm.validate():
            usuario = frm.usuario_válido

            login_user(usuario)

            flash(f"El usuario {usuario.nombre} ha iniciado sesión")

            destino = url_for('principal.página_principal')

            if request.args.get('next'):
                destino = request.args.get('next')

            return redirect(destino)

        else:
            flash("Ha ocurrido un error en el formulario", "error")

    return render_template('iniciar-sesión.html', frm = frm)

@bp.get('/cerrar-sesión')
def cerrar_sesión():
    logout_user()

    flash("El usuario ha cerrado sesión")
    return redirect(url_for('principal.página_principal'))

@bp.route('/editar-usuario', methods=['GET', 'POST'])
@login_required
def editar_usuario():
    frm = EditarUsuario(obj = current_user)

    if request.method == 'POST':
        if frm.validate():
            current_user.nombre = frm.nombre.data
            current_user.usuario = frm.usuario.data
            current_user.correo_electrónico = frm.correo_electrónico.data
            if frm.foto.data:
                current_user.tiene_foto = True

            db.session.add(current_user)
            db.session.commit()

            if frm.foto.data:
                with Image.open(frm.foto.data) as foto:

                    ancho, alto = foto.size
                    # 100 / 50 =  2
                    # 50 / 100 = 0.5
                    # 100 / 100 = 1
                    proporción: float = ancho / alto

                    if proporción > 1:
                        # La foto es horizontal
                        lado = alto
                    else:
                        lado = ancho

                    c_ancho = ancho // 2 - lado // 2
                    c_alto = alto // 2 - lado // 2

                    coordenadas = (
                        c_ancho,
                        c_alto,
                        c_ancho + lado,
                        c_alto + lado
                    )

                    foto = foto.crop(coordenadas)

                    foto.thumbnail((512, 512))
                    foto.save(f'static/imgs/avatares/{current_user.id}.jpg')

                #frm.foto.data.save(f'static/imgs/avatares/{current_user.id}.jpg')

            flash("El usuario ha sido modificado")

            return redirect(url_for('página_principal'))
        else:
            flash("Hubo un error en el formulario")


    return render_template('editar-usuario.html', frm = frm)



@bp.get('/post/<int:codigo>')
def mostrar_post(codigo):
    post = posts[codigo]

    return render_template('mostrar_post.html', post = post)


@bp.delete('/post/<int:id>')
def borrar_post(id):
    post = db.session.get(Post, id)

    if not post:
        return 'El post no existe!', 404

    db.session.delete(post)
    db.session.commit()

    return ''
