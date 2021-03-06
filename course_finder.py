import requests
from requests.exceptions import HTTPError
from pydal import DAL, Field

def main():
    controller = DatabaseController()
    print(controller.get_course_names()[0][0])
    print(controller.get_prefixes())

class DatabaseController:
    def update_database(self):
        db = DAL('sqlite://courses.db', folder='dbs')
        try:
            response = requests.get('http://localhost:5000/api/v1.0/courses/all/2000');
            response.raise_for_status()
            jsonResponse = response.json()

            db.define_table('courses', Field('class_id', type='integer'), Field('class_name'), Field('date_time'),
                            Field('descriptive_link'), Field('enrolled'), Field('instructor'), Field('link_sources'),
                            Field('location'), Field('status'))
            for key in jsonResponse:
                db.courses.insert(class_id=key['class_id'], class_name=key['class_name'], date_time=key['date_time'],
                                  descriptive_link=key['descriptive_link'], enrolled=key['enrolled'],
                                  instructor=key['instructor'], link_sources=key['link_sources'],
                                  location=key['location'],
                                  status=key['status'])
            rows = db().select(db.courses.ALL)

        finally:
            if db:
                db.close()

    def find_course(self, course_name=None, class_id=None, instructor=None):
        db = DAL('sqlite://courses.db', folder='dbs')
        db.define_table('courses', Field('class_id', type='integer'), Field('class_name'), Field('date_time'),
                        Field('descriptive_link'), Field('enrolled'), Field('instructor'), Field('link_sources'),
                        Field('location'), Field('status'))
        if(course_name != None):
            rows = db(db.courses.class_name.like('%'+course_name+'%')).select()
            if len(rows) > 0 and class_id != None:
                return db(db.courses.class_name.like('%'+course_name+'%') and db.courses.class_id == class_id).select().first()
            elif len(rows) > 0 and instructor != None:
                return db(db.courses.class_name.like('%'+course_name+'%') and db.courses.instructor == instructor).select().first()
            else:
                return rows.first()
        elif(class_id != None):
            rows = db(db.courses.class_id == class_id).select()
            return rows.first()
        else:
            return None

    def get_course_names(self, prefix=None):
        db = DAL('sqlite://courses.db', folder='dbs')
        db.define_table('courses', Field('class_id', type='integer'), Field('class_name'), Field('date_time'),
                        Field('descriptive_link'), Field('enrolled'), Field('instructor'), Field('link_sources'),
                        Field('location'), Field('status'))
        if(prefix != None):
            return db.executesql('SELECT DISTINCT class_name FROM courses WHERE class_name LIKE ' + prefix + '%')
        else:
            return db.executesql('SELECT DISTINCT class_name FROM courses')

    def get_prefixes(self):
        db = DAL('sqlite://courses.db', folder='dbs')
        db.define_table('courses', Field('class_id', type='integer'), Field('class_name'), Field('date_time'),
                        Field('descriptive_link'), Field('enrolled'), Field('instructor'), Field('link_sources'),
                        Field('location'), Field('status'))

        course_names = self.get_course_names()
        prefixes = []
        for name in course_names:
            if name[0].split()[0] not in prefixes:
                prefixes.append(name[0].split()[0])
        return prefixes

if __name__ == '__main__':
    main()


