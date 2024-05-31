from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, EmailField, Form
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Email

from sqlalchemy import select
from model import db, Usuario

from flask_login import current_user


class NuevoUsuarioApi(Form):
    nombre = StringField("Nombre completo", validators = [
        DataRequired()
    ])
    usuario = StringField("Nombre de usuario", validators = [
        DataRequired()
    ])
    correo_electrónico = EmailField("Correo electrónico", validators = [
        Email(message = "El correo electrónico es inválido"),
        DataRequired()
    ])
    contraseña = PasswordField("Contraseña", validators = [
        DataRequired(),
        Length(min = 6, message = "La contraseña debe tener al menos 6 caracteres"),
    ])

    def validate_usuario(self, campo):
        dummy = db.session.scalars(
            select(Usuario).where(Usuario.usuario == campo.data)
        ).first()

        if dummy:
            raise ValidationError("Ya existe un usuario con ese... usuario")

class NuevoUsuario(NuevoUsuarioApi, FlaskForm):
    contraseña_nuevamente = PasswordField("Contraseña, nuevamente", validators = [
        DataRequired(),
        Length(min = 6, message = "La contraseña debe tener al menos 6 caracteres"),
        EqualTo("contraseña", message = "Las contraseñas deben coincidir"),
    ])


class IniciarSesiónApi(Form):
    usuario = StringField("Nombre de usuario", validators = [
        DataRequired()
    ])
    contraseña = PasswordField("Contraseña", validators = [
        DataRequired(),
    ])

    def validate_usuario(self, campo_usuario):
        usuario = Usuario.obtener_usuario_desde_credenciales(
            campo_usuario.data,
            self.contraseña.data,
        )

        if usuario is None:
            raise ValidationError(f"Usuario {campo_usuario.data} o contraseña es inválida")

        self.usuario_válido = usuario

class IniciarSesión(IniciarSesiónApi, FlaskForm):
    pass


class EditarUsuario(FlaskForm):
    nombre = StringField("Nombre completo", validators = [
        DataRequired()
    ])
    usuario = StringField("Nombre de usuario", validators = [
        DataRequired()
    ])
    correo_electrónico = EmailField("Correo electrónico", validators = [
    ])

    foto = FileField("Selecciona una imágen para la foto", validators = [
        FileAllowed(['jpg', 'png'])
    ])

    def validate_usuario(self, campo_usuario):
        if current_user.usuario != campo_usuario.data:
            dummy = db.session.scalars(
                select(Usuario).where(Usuario.usuario == campo_usuario.data)
            ).first()

            if dummy:
                raise ValidationError("El nombre de usuario ya está siendo usado")


