#  		test_views.py			Jun 20, 2026
#  				Adrián E. Córdoba [software.dynamicmcs@gmail.com]
#
#  Copyright (C) 2026
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
from datetime import date

from django.contrib.auth.models import Permission, Group
from django.test import TestCase
from django.urls import reverse
from partners.models import Country, State, City, Address, Person, Partner
from users.models import User


class UserCreationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Persons
        country = Country.objects.create(name='Country_1')
        state = State.objects.create(name='State_1', country=country)
        city = City.objects.create(name='City_1', state=state)
        address = Address.objects.create(address='Address_1', zip_code='000001', city=city, phone='55550001')
        person_1 = Person.objects.create(identification='identification_1', id_number=10000001,
                                         social_security='100000/01', last_name='Last_name_1',
                                         first_name='First_name_1 Middle_name_1', email='last_name_1@mail.com',
                                         birthdate='1960-01-01', gender='male', address=address, cellphone='0015550001')
        person_2 = Person.objects.create(identification='identification_1', id_number=10000002,
                                         social_security='100000/02', last_name='Last_name_2',
                                         first_name='First_name_2 Middle_name_2', email='last_name_2@mail.com',
                                         birthdate='1960-01-02', gender='male', address=address, cellphone='0015550002')
        person_3 = Person.objects.create(identification='identification_1', id_number=10000003,
                                         social_security='100000/03', last_name='Last_name_3',
                                         first_name='First_name_3 Middle_name_3', email='last_name_3@mail.com',
                                         birthdate='1960-01-03', gender='female', address=address,
                                         cellphone='0015550003')
        # Partners
        partner_1 = Partner.objects.create(person=person_1, partner_number=10001, incorporation='2026-01-01',
                                           position='position_1', status='status_1')
        partner_2 = Partner.objects.create(person=person_2, partner_number=10002, incorporation='2026-01-02',
                                           position='position_1', status='status_1')
        Partner.objects.create(person=person_3, partner_number=10003, incorporation='2026-01-03',
                               position='position_1', status='status_1')
        # Users and permissions
        staff_user = User.objects.create_user(name='staff_user', partner=partner_1, password='password_1')
        User.objects.create_user(name='user', partner=partner_2, password='password_1')
        permission_codenames = ['add_user', 'view_user']
        permission = Permission.objects.filter(codename__in=permission_codenames)
        staff_user.user_permissions.add(*permission)
        Group.objects.create(name='Management')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('create-user'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/users/create/')

    def test_logged_in_forbiden_resource(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('create-user'))
        self.assertEqual(response.status_code, 403)

    def test_logged_authorized_user_get_correct_template(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('create-user'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'staff_user')
        self.assertTemplateUsed(response, 'users/user_form.html')

    def test_post_user_saved(self):
        self.client.login(username='staff_user', password='password_1')
        data = {'name': 'test_user', 'partner': Partner.objects.last().id, 'is_active': True, 'is_staff': False}
        response = self.client.post(reverse('create-user'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users'))
        self.assertEqual(User.objects.count(), 3)
        usernames_list = [user.name for user in User.objects.all()]
        self.assertIn('test_user', usernames_list)


class UserUpdateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Persons
        country = Country.objects.create(name='Country_1')
        state = State.objects.create(name='State_1', country=country)
        city = City.objects.create(name='City_1', state=state)
        address = Address.objects.create(address='Address_1', zip_code='000001', city=city, phone='55550001')
        person_1 = Person.objects.create(identification='identification_1', id_number=10000001,
                                         social_security='100000/01', last_name='Last_name_1',
                                         first_name='First_name_1 Middle_name_1', email='last_name_1@mail.com',
                                         birthdate='1960-01-01', gender='male', address=address, cellphone='0015550001')
        person_2 = Person.objects.create(identification='identification_1', id_number=10000002,
                                         social_security='100000/02', last_name='Last_name_2',
                                         first_name='First_name_2 Middle_name_2', email='last_name_2@mail.com',
                                         birthdate='1960-01-02', gender='male', address=address, cellphone='0015550002')
        # Partners
        partner_1 = Partner.objects.create(person=person_1, partner_number=10001, incorporation='2026-01-01',
                                           position='position_1', status='status_1')
        partner_2 = Partner.objects.create(person=person_2, partner_number=10002, incorporation='2026-01-02',
                                           position='position_1', status='status_1')
        # Users and permissions
        staff_user = User.objects.create_user(name='staff_user', partner=partner_1, password='password_1')
        User.objects.create_user(name='user', partner=partner_2, password='password_1')
        permission_codenames = ['change_user', 'view_user']
        permission = Permission.objects.filter(codename__in=permission_codenames)
        staff_user.user_permissions.add(*permission)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('update-user', args=[User.objects.last().id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/users/update/{User.objects.last().id}')

    def test_logged_in_forbiden_resource(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('update-user', args=[User.objects.last().id]))
        self.assertEqual(response.status_code, 403)

    def test_logged_authorized_user_get_correct_template(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('update-user', args=[User.objects.last().id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'staff_user')
        self.assertTemplateUsed(response, 'users/user_form.html')

    def test_correct_instance(self):
        self.client.login(username='staff_user', password='password_1')
        url = reverse('update-user', kwargs={'pk': User.objects.last().id})
        response = self.client.get(url)
        form = response.context['form']
        self.assertFalse(response.context['create'])
        self.assertEqual(form.fields['name'].initial, User.objects.last().name)


class UsersListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):  # Persons
        country = Country.objects.create(name='Country_1')
        state = State.objects.create(name='State_1', country=country)
        city = City.objects.create(name='City_1', state=state)
        for index in range(15):
            suffix = f'{index:02d}'
            address = Address.objects.create(address='Address_' + suffix, zip_code='000001', city=city,
                                             phone='555500' + suffix)
            person = Person.objects.create(identification='identification_1', id_number=100000 + index,
                                           social_security='100000/' + suffix, last_name='Last_name_' + suffix,
                                           first_name='First_name_' + suffix + ' Middle_name_' + suffix,
                                           email='last_name_' + suffix + '@mail.com', birthdate='1960-01-01',
                                           gender='male', address=address, cellphone='00155500' + suffix)
            partner = Partner.objects.create(person=person, partner_number=10000 + index, incorporation=date.today(),
                                             position='position_1', status='status_1')
            User.objects.create_user(name='user_' + suffix, partner=partner, password='password_' + suffix)
        # Users and permissions
        partner_1 = Partner.objects.get(partner_number=10000)
        User.objects.get(partner=partner_1).delete()
        staff_user = User.objects.create_user(name='staff_user', partner=partner_1, password='password_1')
        permission = Permission.objects.get(codename='view_user')
        staff_user.user_permissions.add(permission)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/users/')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_list.html')

    def test_pagination_is_ten(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['users_no_admin']), 10)

    def test_lists_all_users(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('users') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['users_no_admin']), 5)


class UserDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Persons
        country = Country.objects.create(name='Country_1')
        state = State.objects.create(name='State_1', country=country)
        city = City.objects.create(name='City_1', state=state)
        address = Address.objects.create(address='Address_1', zip_code='000001', city=city, phone='55550001')
        person_1 = Person.objects.create(identification='identification_1', id_number=10000001,
                                         social_security='100000/01', last_name='Last_name_1',
                                         first_name='First_name_1 Middle_name_1', email='last_name_1@mail.com',
                                         birthdate='1960-01-01', gender='male', address=address, cellphone='0015550001')
        person_2 = Person.objects.create(identification='identification_1', id_number=10000002,
                                         social_security='100000/02', last_name='Last_name_2',
                                         first_name='First_name_2 Middle_name_2', email='last_name_2@mail.com',
                                         birthdate='1960-01-02', gender='male', address=address, cellphone='0015550002')
        # Partners
        partner_1 = Partner.objects.create(person=person_1, partner_number=10001, incorporation='2026-01-01',
                                           position='position_1', status='status_1')
        partner_2 = Partner.objects.create(person=person_2, partner_number=10002, incorporation='2026-01-02',
                                           position='position_1', status='status_1')
        # Users and permissions
        staff_user = User.objects.create_user(name='staff_user', partner=partner_1, password='password_1')
        User.objects.create_user(name='user', partner=partner_2, password='password_1')
        permission = Permission.objects.get(codename='view_user')
        staff_user.user_permissions.add(permission)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('user-detail', args=[User.objects.last().id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/users/{User.objects.last().id}')

    def test_logged_in_forbiden_resource(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('user-detail', args=[User.objects.last().id]))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_user_get_correct_template(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('user-detail', args=[User.objects.last().id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'staff_user')
        self.assertTemplateUsed(response, 'users/user_detail.html')


class UserDeleteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Persons
        country = Country.objects.create(name='Country_1')
        state = State.objects.create(name='State_1', country=country)
        city = City.objects.create(name='City_1', state=state)
        address = Address.objects.create(address='Address_1', zip_code='000001', city=city, phone='55550001')
        person_1 = Person.objects.create(identification='identification_1', id_number=10000001,
                                         social_security='100000/01', last_name='Last_name_1',
                                         first_name='First_name_1 Middle_name_1', email='last_name_1@mail.com',
                                         birthdate='1960-01-01', gender='male', address=address, cellphone='0015550001')
        person_2 = Person.objects.create(identification='identification_1', id_number=10000002,
                                         social_security='100000/02', last_name='Last_name_2',
                                         first_name='First_name_2 Middle_name_2', email='last_name_2@mail.com',
                                         birthdate='1960-01-02', gender='male', address=address, cellphone='0015550002')
        # Partners
        partner_1 = Partner.objects.create(person=person_1, partner_number=10001, incorporation='2026-01-01',
                                           position='position_1', status='status_1')
        partner_2 = Partner.objects.create(person=person_2, partner_number=10002, incorporation='2026-01-02',
                                           position='position_1', status='status_1')
        # Users and permissions
        staff_user = User.objects.create_user(name='staff_user', partner=partner_1, password='password_1')
        User.objects.create_user(name='user', partner=partner_2, password='password_1')
        permission_codenames = ['delete_user', 'view_user']
        permission = Permission.objects.filter(codename__in=permission_codenames)
        staff_user.user_permissions.add(*permission)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('delete-user', args=[User.objects.last().id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/users/delete/{User.objects.last().id}')

    def test_logged_in_forbiden_resource(self):
        self.client.login(username='user', password='password_1')
        response = self.client.get(reverse('delete-user', args=[User.objects.last().id]))
        self.assertEqual(response.status_code, 403)

    def test_authorized_user_get_correct_template(self):
        self.client.login(username='staff_user', password='password_1')
        response = self.client.get(reverse('delete-user', args=[User.objects.last().id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'staff_user')
        self.assertTemplateUsed(response, 'users/user_confirm_delete.html')

    def test_correct_user_deleted(self):
        self.client.login(username='staff_user', password='password_1')
        user_id = User.objects.last().id
        response = self.client.post(reverse('delete-user', args=[user_id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/')
        self.assertNotIn(user_id, [user.id for user in User.objects.all()])

