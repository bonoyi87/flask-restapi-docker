"""empty message

Revision ID: ff5f9dcc8a38
Revises: 80e7eecc7513
Create Date: 2019-05-01 16:31:59.001969

"""
from alembic import op
import sqlalchemy as sa
import re

# revision identifiers, used by Alembic.


revision = 'ff5f9dcc8a38'
down_revision = '80e7eecc7513'
branch_labels = None
depends_on = None

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']


def clean_str(_str):
    _str = re.sub(r"\(주\)", "", _str)
    _str = re.sub(r"[\(\).]", "", _str)
    return _str.replace(" ", "")


def index_str(str, only_chosung=False):
    r_lst = []
    for w in list(str.strip()):
        if '가' <= w <= '힣':
            ch1 = (ord(w) - ord('가')) // 588
            ch2 = ((ord(w) - ord('가')) - (588 * ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588 * ch1) - 28 * ch2
            if only_chosung:
                r_lst.append(CHOSUNG_LIST[ch1])
            else:
                r_lst.append(CHOSUNG_LIST[ch1])
                r_lst.append(JUNGSUNG_LIST[ch2])
                r_lst.append(JONGSUNG_LIST[ch3])
        else:
            r_lst.append(w)
    return ''.join(r_lst) if r_lst else ''


def upgrade():
    migrate()


def get_initial_index(val):
    return index_str(val, only_chosung=True)


def get_phoneme_index(val):
    return index_str(val)


def migrate():
    import csv

    from wanted.extensions import db
    from wanted.company.models import Company, CompanyName, CompanyTag, SearchCompany
    from wanted.company.models.company import Tag

    db.engine.execute("ALTER DATABASE wanted DEFAULT CHARACTER SET utf8")
    with open('wanted_temp_data.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            company_ko = row.get('company_ko')
            company_en = row.get('company_en')
            company_ja = row.get('company_ja')
            tag_ko = row.get('tag_ko')
            tag_en = row.get('tag_en')
            tag_ja = row.get('tag_ja')
            master_company = Company()
            db.session.add(master_company)
            db.session.commit()

            master_company_id = master_company.id
            results = []
            if company_ko:
                results.append(CompanyName(company_id=master_company_id,
                                           name=company_ko,
                                           lang='ko'
                                           ))
            if company_en:
                results.append(CompanyName(company_id=master_company_id,
                                           name=company_en,
                                           lang='en'
                                           ))
            if company_ja:
                results.append(CompanyName(company_id=master_company_id,
                                           name=company_ja,
                                           lang='ja'
                                           ))
            if tag_ko:
                for tk in tag_ko.split('|'):
                    tag = Tag.query.filter_by(tag=tk).first()
                    if not tag:
                        tag = Tag(tag=tk, lang='ko')
                        db.session.add(tag)
                        db.session.commit()

                    results.append(CompanyTag(company_id=master_company_id,
                                              tag_id=tag.id))
            if tag_en:
                for te in tag_en.split('|'):
                    tag = Tag.query.filter_by(tag=te).first()
                    if not tag:
                        tag = Tag(tag=te, lang='en')
                        db.session.add(tag)
                        db.session.commit()

                    results.append(CompanyTag(company_id=master_company_id,
                                              tag_id=tag.id))
            if tag_ja:
                for tj in tag_ja.split('|'):
                    tag = Tag.query.filter_by(tag=tj).first()
                    if not tag:
                        tag = Tag(tag=tj, lang='ja')
                        db.session.add(tag)
                        db.session.commit()
                    results.append(CompanyTag(company_id=master_company_id,
                                              tag_id=tag.id))
            if company_ko:
                company_ko = clean_str(company_ko)
                initial_index = get_initial_index(company_ko)
                phoneme_index = get_phoneme_index(company_ko)
                results.append(SearchCompany(company_id=master_company_id,
                                             initial_index=initial_index,
                                             phoneme_index=phoneme_index,
                                             )
                               )
            if company_en:
                company_en = clean_str(company_en)

                initial_index = get_initial_index(company_en)
                phoneme_index = get_phoneme_index(company_en)
                results.append(SearchCompany(company_id=master_company_id,
                                             initial_index=initial_index,
                                             phoneme_index=phoneme_index,
                                             )
                               )

            if company_ja:
                company_ja = clean_str(company_ja)
                initial_index = get_initial_index(company_ja)
                phoneme_index = get_phoneme_index(company_ja)
                results.append(SearchCompany(company_id=master_company_id,
                                             initial_index=initial_index,
                                             phoneme_index=phoneme_index,
                                             )
                               )
            db.session.add_all(results)

        try:
            db.session.flush()
        except Exception as e:
            print(e)
            db.session.rollback()


def downgrade():
    pass
