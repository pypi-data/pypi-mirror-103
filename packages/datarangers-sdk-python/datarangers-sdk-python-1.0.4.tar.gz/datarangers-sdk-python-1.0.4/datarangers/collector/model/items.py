"""
Copyright 2020 Beijing Volcano Engine Technology Co., Ltd.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
Apache License, Version 2.0
Home page of The Apache Software Foundation
"""


class Items(object):
    def __init__(self, item_id, item_name):
        self.item_id = item_id
        self.item_name = item_name

    def get_item_id(self):
        return self.item_id

    def get_item_name(self):
        return self.item_name

    def set_item_id(self, item_id):
        self.item_id = item_id
        return self

    def set_item_name(self, item_name):
        self.item_name = item_name
        return self

    def get_json(self):
        return self.__dict__
