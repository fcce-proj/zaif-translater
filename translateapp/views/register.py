import logging
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid

from ..models import User, Phrase


log = logging.getLogger(__name__)


@view_config(route_name='home', renderer='../templates/register.pt')
@view_config(route_name='register', renderer='../templates/register.pt')
def register_view(request):
    log.debug('+++++++++[register get]+++++++++')
    userid = authenticated_userid(request)
    login_user = request.dbsession.query(User).filter(User.id == userid).first()

    if login_user is None:
        return HTTPFound(location=request.route_url('login'))

    language_list = request.dbsession.query(Phrase).all()
    return dict(login_user=login_user, Language_list=language_list)


@view_config(route_name='register', request_method='POST', renderer='json')
def register(request):
    log.debug('+++++++++[register post]+++++++++')
    japanese = request.params['ja']
    english = request.params['en']
    chinese = request.params['zh']

    if japanese is None:
        return dict(key=japanese, register_flag=False)

    phrases = request.dbsession.query(Phrase).filter(Phrase.key_lang == japanese).all()
    if japanese in phrases:
        log.debug('already registered: {}'.format(japanese))
        return dict(key=japanese, register_flag=False)

    new_phrase = Phrase(key_lang=japanese, ja=japanese, en=english, zh=chinese)
    request.dbsession.add(new_phrase)
    log.debug('registered: {}'.format(japanese))
    return dict(key=japanese, register_flag=True)


@view_config(route_name='edit', request_method='POST', renderer='json')
def edit(request):
    log.debug('+++++++++[edit]+++++++++')
    edit_id = int(request.params['edit_id'])
    new_key_lang = request.params['edit_key']
    new_japanese = request.params['edit_ja']
    new_english = request.params['edit_en']
    new_chinese = request.params['edit_zh']

    request.dbsession.query(Phrase).filter(Phrase.id == edit_id).update({
        Phrase.key_lang: new_key_lang,
        Phrase.ja: new_japanese,
        Phrase.en: new_english,
        Phrase.zh: new_chinese,
    })


@view_config(route_name='search', request_method='POST', renderer='../templates/register.pt')
def search(request):
    log.debug('+++++++++[search]+++++++++')
    search_words = request.params['search']

    for key in ('key_lang', 'ja', 'en', 'zh'):
        phrases = request.dbsession.query(Phrase).filter(
            eval("Phrase." + key + ".ilike('%" + search_words + "%')")).all()
        if phrases:
            return dict(Phrase=phrases)

    return dict(Phrase=[])