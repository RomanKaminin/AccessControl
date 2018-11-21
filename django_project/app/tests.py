import unittest
from app.models import AccessRequest
from app.views import AlphaList

class AccessModelTest(unittest.TestCase):

    def create_access_request(self):
        self.access = AccessRequest.objects.create(
            space_name="главный офис",
            name="Иванов Иван Иванович",
            type="manager",
            access="yes",
            date="2018-10-1",
        )
        return self.access

    def test_access_request_creation(self):
        new_access = self.create_access_request()
        self.assertTrue(isinstance(new_access, AccessRequest))



class AlphaListTest(unittest.TestCase):

    def test_split_alph_list_one(self):
        variants = (
            (
                [
                    u'А', u'Б', u'В', u'К'
                ],
                1,
                [
                    [u'А', u'Б', u'В', u'К']
                ]
             ),
            (
                [
                    u'А', u'Б', u'В', u'Д',
                    u'Е', u'Ё', u'Ж', u'З'
                ],
                2,
                [
                    [u'А', u'Б', u'В', u'Д'],
                    [u'Е', u'Ё', u'Ж', u'З']
                ]
            ),
            (
                [
                    u'Р', u'С', u'Т', u'У',
                    u'Ф', u'Х', u'Ц', u'Ч',
                    u'Ш', u'Щ', u'Э'
                ],
                3,
                [
                    [u'Р', u'С', u'Т', u'У'],
                    [u'Ф', u'Х', u'Ц', u'Ч'],
                    [u'Ш', u'Щ', u'Э']
                ]
            ),
            (
                [
                    u'Д', u'Е', u'Ё', u'Ж',
                    u'З', u'И', u'К', u'Л',
                    u'Ф', u'Х', u'Ц', u'Ч',
                    u'Ш', u'Щ', u'Ы', u'Ъ'
                ],
                4,
                [
                    [u'Д', u'Е', u'Ё', u'Ж'],
                    [u'З', u'И', u'К', u'Л'],
                    [u'Ф', u'Х', u'Ц', u'Ч'],
                    [u'Ш', u'Щ', u'Ы', u'Ъ']
                ]
            ),
            (
                [
                    u'Д', u'Е', u'Ё', u'Ж', u'З',
                    u'И', u'К', u'Л', u'М', u'Н',
                    u'О', u'П', u'Ф', u'Х', u'Ц',
                    u'Ч', u'Ш', u'Щ', u'Ы', u'Ъ',
                    u'Ь', u'Э'
                ],
                5,
                [
                    [u'Д', u'Е', u'Ё', u'Ж', u'З'],
                    [u'И', u'К', u'Л', u'М', u'Н'],
                    [u'О', u'П', u'Ф', u'Х'],
                    [u'Ц', u'Ч', u'Ш', u'Щ'],
                    [u'Ы', u'Ъ', u'Ь', u'Э']
                ]
            ),
            (
                [
                    u'А', u'Б', u'В', u'Г', u'Д', u'Е', u'Ё', u'Ж', u'З', u'И', u'К',
                    u'Л', u'М', u'Н', u'О', u'П', u'Ф', u'Х', u'Ц', u'Ч', u'Ш', u'Щ',
                    u'Ы', u'Ъ', u'Ь', u'Э', u'Ю', u'Я'
                ],
                6,
                [
                    [u'А', u'Б', u'В', u'Г', u'Д'],
                    [u'Е', u'Ё', u'Ж', u'З', u'И'],
                    [u'К', u'Л', u'М', u'Н', u'О'],
                    [u'П', u'Ф', u'Х', u'Ц', u'Ч'],
                    [u'Ш', u'Щ', u'Ы', u'Ъ'],
                    [u'Ь', u'Э', u'Ю', u'Я']
                ]
            ),
            (
                [
                    u'А', u'Б', u'В', u'Г', u'Д', u'Е', u'Ё', u'Ж', u'З', u'И', u'Й',
                    u'К', u'Л', u'М', u'Н', u'О', u'П', u'Р', u'С', u'Т', u'У', u'Ф',
                    u'Х', u'Ц', u'Ч', u'Ш', u'Щ', u'Ъ', u'Ы', u'Ь', u'Э', u'Ю', u'Я'
                ],
                7,
                [
                    [u'А', u'Б', u'В', u'Г', u'Д'],
                    [u'Е', u'Ё', u'Ж', u'З', u'И'],
                    [u'Й', u'К', u'Л', u'М', u'Н'],
                    [u'О', u'П', u'Р', u'С', u'Т'],
                    [u'У', u'Ф', u'Х', u'Ц', u'Ч'],
                    [u'Ш', u'Щ', u'Ъ', u'Ы'],
                    [u'Ь', u'Э', u'Ю', u'Я']
                ]
            )
        )
        for objects_alphabet, count_lists, result_list in variants:
            with self.subTest(i=count_lists):
                lists_vals = list(AlphaList.split_alph_list(self, objects_alphabet, count_lists))
                self.assertEqual(lists_vals, result_list)

