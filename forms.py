from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields import StringField, PasswordField, DateField, RadioField,FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, length, equal_to


class RegisterForm(FlaskForm):
    username = StringField("შეიყვანე იუზერნეიმი", validators=[DataRequired()])
    password = PasswordField("მოიფიქრე პაროლი", validators=[DataRequired(), length(min=8, max=20)])
    repeat_password = PasswordField("გაიმეორე პაროლი", validators=[DataRequired(), equal_to("password")])

    submit = SubmitField("რეგისტრაცია")


class LoginForm(FlaskForm):
    username = StringField()
    password = PasswordField()

    login = SubmitField("შესვლა")

class ProductForm(FlaskForm):
    img = FileField("აირჩიეთ პროფილის ფოტო")
    name = StringField("ჩაწერე პროდუქტის სახელი")
    price = FloatField("ჩაწერე ფასი")

    submit = SubmitField("შექმნა")