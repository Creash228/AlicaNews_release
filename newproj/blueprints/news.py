from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from extensions import db
from forms.news_new import NewsForm
from services.news_service import NewsService

news_bp = Blueprint('news', __name__)


@news_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = NewsForm()
    if form.validate_on_submit():
        news = NewsService.create(
            db.session,
            title=form.title.data,
            content=form.content.data,
            author_id=current_user.id,
            is_private=form.is_private.data
        )
        if form.photo.data:
            image_path = NewsService.save_image(form.photo.data, news.id)
            if image_path:
                news.image = image_path
                db.session.commit()
        flash('Новость добавлена!')
        return redirect(url_for('main.index'))
    return render_template('add_news.html', form=form, title='Добавить новость')


@news_bp.route('/<int:news_id>')
def detail(news_id):
    news = NewsService.get_by_id(db.session, news_id)
    if not news:
        abort(404)
    if news.is_private and (not current_user.is_authenticated or current_user.id != news.author_id):
        abort(403)
    return render_template('news_detail.html', news=news)


@news_bp.route('/<int:news_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(news_id):
    news = NewsService.get_by_id(db.session, news_id)
    if not news or news.author_id != current_user.id:
        abort(404)
    
    form = NewsForm(obj=news)
    if form.validate_on_submit():
        image_path = news.image
        if form.photo.data:
            new_image = NewsService.save_image(form.photo.data, news.id)
            if new_image:
                image_path = new_image
        
        NewsService.update(
            db.session,
            news_id,
            title=form.title.data,
            content=form.content.data,
            is_private=form.is_private.data,
            image=image_path
        )
        flash('Новость обновлена')
        return redirect(url_for('news.detail', news_id=news_id))
    
    return render_template('add_news.html', form=form, title='Редактировать новость')


@news_bp.route('/<int:news_id>/delete')
@login_required
def delete(news_id):
    news = NewsService.get_by_id(db.session, news_id)
    if not news or news.author_id != current_user.id:
        abort(404)
    
    NewsService.delete(db.session, news_id)
    flash('Новость удалена')
    return redirect(url_for('main.index'))


@news_bp.route('/my')
@login_required
def my_news():
    news_list = NewsService.get_by_author(db.session, current_user.id)
    return render_template('index.html', news_list=news_list, title='Мои новости')
