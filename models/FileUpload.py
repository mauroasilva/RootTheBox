# -*- coding: utf-8 -*-
'''
Created on Mar 15, 2012

@author: moloch

    Copyright 2012 Root the Box

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
'''


from models import dbsession
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import synonym
from sqlalchemy.types import Unicode, Integer
from models.BaseGameObject import BaseObject
from string import ascii_letters, digits


class FileUpload(BaseObject):

    _file_name = Column(Unicode(64), nullable=False)
    file_name = synonym('_file_name', descriptor=property(
        lambda self: self._file_name,
        lambda self, file_name: setattr(
            self, '_file_name', self.__class__.filter_string(file_name, ".-_"))
    ))
    content = Column(Unicode(255), nullable=False)
    uuid = Column(Unicode(64), unique=True, nullable=False)
    description = Column(Unicode(1024), nullable=False)
    byte_size = Column(Integer, nullable=False)
    team_id = Column(Integer, ForeignKey('team.id'), nullable=False)

    @classmethod
    def all(cls):
        ''' Returns a list of all objects in the database '''
        return dbsession.query(cls).all()

    @classmethod
    def by_id(cls, ident):
        ''' Returns a the object with id of ident '''
        return dbsession.query(cls).filter_by(id=ident).first()

    @classmethod
    def by_uuid(cls, uuid):
        ''' Return the user object whose uuid is "uuid" '''
        return dbsession.query(cls).filter_by(uuid=unicode(uuid)).first()

    @classmethod
    def by_file_name(cls, file_name):
        ''' Return the user object whose file name is "file_name" '''
        return dbsession.query(cls).filter_by(
            file_name=unicode(file_name)
        ).first()

    @classmethod
    def filter_string(cls, string, extra_chars=''):
        char_white_list = ascii_letters + digits + extra_chars
        return filter(lambda char: char in char_white_list, string)

    def __repr__(self):
        return u'<FileUpload - name: %s, size: %s>' % (self.file_name, self.byte_size)
