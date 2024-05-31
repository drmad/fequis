from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, Integer, String, Text, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from flask_login import UserMixin

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

import datetime

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key = True)
    nombre: Mapped[str] = mapped_column(String(128))
    usuario: Mapped[str] = mapped_column(String(16), unique = True)
    correo_electrónico: Mapped[str] = mapped_column(String(256))
    contraseña: Mapped[str] = mapped_column(String(256))
    tiene_foto: Mapped[bool] = mapped_column(default = False)
    es_administrador: Mapped[bool] = mapped_column(default = False)
    posts = relationship('Post', back_populates = 'usuario')

    def crear_usuario(nombre, usuario, correo_electrónico, contraseña):
        ph = PasswordHasher()
        db.session.add(
            Usuario(
                nombre = nombre,
                usuario = usuario,
                correo_electrónico = correo_electrónico,
                contraseña = ph.hash(contraseña)
            )
        )
        db.session.commit()

    def obtener_usuario_desde_credenciales(usuario, contraseña):
        usuario = db.session.scalars(
            select(Usuario).where(Usuario.usuario == usuario)
        ).first()

        if not usuario:
            return None

        ph = PasswordHasher()
        try:
            ph.verify(usuario.contraseña, contraseña)
        except VerifyMismatchError:
            return None

        return usuario

    def obtener_usuario(id: int):
        return db.session.get(Usuario, id)

    def obtener_usuario_desde_usuario(usuario: str):
        return db.session.scalars(
            select(Usuario).where(Usuario.usuario == usuario)
        ).first()


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuario.id'))
    usuario = relationship(Usuario, back_populates = 'posts')
    fecha: Mapped[datetime.datetime]
    cuerpo = mapped_column(Text)
    likes: Mapped[int] = mapped_column(default = 0)

    def obtener_posts():
        return db.session.query(Post).order_by(Post.fecha.desc())

    def crear_post(usuario: Usuario, cuerpo):
        nuevo_post = Post(
            usuario = usuario,
            fecha = datetime.datetime.now(),
            cuerpo = cuerpo
        )

        db.session.add(nuevo_post)
        db.session.commit()

        return nuevo_post

    def obtener_post(id: int):
        return db.session.get(Post, id)

    def borrar_post(self):
        db.session.delete(self)
        db.session.commit()
