from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, Email, EqualTo, ValidationError
from flask_ckeditor import CKEditorField
from wtforms.widgets.core import TextArea

from database.models import User


class FormRegister(FlaskForm):
    username = StringField('Имя',
                           validators=[DataRequired(message='Введите ваше имя.'
                                                    ),
                                       Length(min=3, max=25,
                                              message='Имя должно содержать от 3 до 25 '
                                                      'символов.'
                                              ),
                                       Regexp('^[А-Яа-яA-Za-z][А-Яа-яA-Za-z0-9_.]*$', 0,
                                              message='Имя должно начинаться с буквы и должно содержать буквы, '
                                                      'цифры, точки или подчеркивания.'
                                              )
                                       ]
                           )
    email = EmailField('Ваша эл. почта',
                       validators=[DataRequired(message='Введите email-адрес.'
                                                ),
                                   Email(message='Некорректный email-адрес.'
                                         )
                                   ]
                       )
    password = PasswordField('Ваш пароль',
                             validators=[DataRequired(message='Введите ваш пароль')]
                             )
    password2 = PasswordField('Проверка пароля',
                              validators=[DataRequired(message='Повторите пароль'
                                                       ),
                                          EqualTo('password',
                                                  message='Пароли не совпадают.'
                                                  )
                                          ]
                              )
    button = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        existing_username = User.query.filter_by(username=username.data).first()
        if existing_username:
            raise ValidationError('Это имя уже занято. Пожалуйста выберите другое имя')

    def validate_email(self, email):
        existing_email = User.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError('Этот email-адрес уже занят. Пожалуйста выберите другой')


class FormLogin(FlaskForm):
    email = EmailField('Ваша эл. почта',
                       validators=[DataRequired(message='Введите email-адрес.'
                                                ),
                                   Email(message='Некорректный email-адрес.'
                                         )
                                   ]
                       )
    password = PasswordField('Введите пароль',
                             validators=[DataRequired(message='Введите ваш пароль')]
                             )
    button = SubmitField('Войти')


class ArticleForm(FlaskForm):
    title = StringField('Заголовок',
                        validators=[DataRequired(message='Напишите заголовок')]
                        )
    intro = StringField('Краткое описание',
                        validators=[DataRequired(message='Введите краткое описание')],
                        widget=TextArea()
                        )
    content = CKEditorField('Текст статьи')
    tag = StringField('Категория', validators=[DataRequired()])
    button = SubmitField('Сохранить')
