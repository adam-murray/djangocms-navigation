from django.contrib.admin.sites import AdminSite
from django.shortcuts import reverse
from django.test import TestCase

from cms.test_utils.testcases import CMSTestCase

from djangocms_navigation.admin import MenuItemAdmin
from djangocms_navigation.models import Menu, MenuContent, MenuItem
from djangocms_navigation.test_utils import factories

from .utils import MockRequest


class MenuContentModelTestCase(TestCase):
    def test_title(self):
        menu_content = factories.MenuContentFactory(root__title="My Title")
        self.assertEqual(menu_content.title, "My Title")


class MenuItemTestCase(CMSTestCase):

    def test_has_add_permission_with_invalid_request(self):
        """
        has_add_permission returns False for request which doesnt contain
        menu_content_id
        """
        ma = MenuItemAdmin(MenuItem, AdminSite())
        request = MockRequest()
        request.user = self.get_superuser()
        self.assertFalse(ma.has_add_permission(request))

    def test_has_add_permission_with_valid_request(self):
        """
        has_add_permission returns True for valid request object containing
        menu_content_id
        """
        ma = MenuItemAdmin(MenuItem, AdminSite())
        request = MockRequest()
        menu_content = factories.MenuContentFactory(root__title="My Title")
        request.menu_content_id = menu_content.id
        request.user = self.get_superuser()
        self.assertTrue(ma.has_add_permission(request))

    def test_has_change_permission_with_invalid_request(self):
        """
        has_change_permission returns False for request which doesnt contain
        menu_content_id
        """
        ma = MenuItemAdmin(MenuItem, AdminSite())
        request = MockRequest()
        request.user = self.get_superuser()
        self.assertFalse(ma.has_change_permission(request))

    def test_has_change_permission_with_valid_request(self):
        """
        has_change_permission returns True for valid request object containing
        menu_content_id
        """
        ma = MenuItemAdmin(MenuItem, AdminSite())
        request = MockRequest()
        menu_content = factories.MenuContentFactory(root__title="My Title")
        request.menu_content_id = menu_content.id
        request.user = self.get_superuser()
        self.assertTrue(ma.has_change_permission(request, None))


class MenuContentFormTestCase(CMSTestCase):

    def test_menucontent_save_model(self):
        self.client.force_login(self.get_superuser())
        self.assertEquals(MenuContent.objects.count(), 0)
        post_data = {"title": "My Title"}
        response = self.client.post(
            reverse("admin:djangocms_navigation_menucontent_add"), post_data
        )

        self.assertRedirects(
            response, reverse("admin:djangocms_navigation_menucontent_changelist")
        )
        self.assertEquals(MenuContent.objects.count(), 1)
        self.assertEqual(Menu.objects.count(), 1)
        self.assertEqual(MenuItem.objects.count(), 1)
        self.assertEqual(MenuItem.objects.all()[0].title, "My Title")