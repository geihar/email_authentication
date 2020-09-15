import unittest
import json
from unittest import mock

from flask import session

from app import app
from models import User, db


class ViewTests(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        db.create_all()
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_index_page_unauthorized(self):
        with self.client as client:

            response = client.get("/")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Отправить ссылку для входа", html)
            self.assertEqual("form" in html, True)
            self.assertNotEqual("token" in session, True)

    def test_get_index_page_authorized(self):
        with self.client as client:

            with client.session_transaction() as session:
                session["token"] = True

            response = client.get("/")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Вы прошли аутентификацию через email", html)
            self.assertEqual("form" in html, False)
            self.assertEqual("token" in session, True)

    def test_get_analytics_page_unauthorized(self):
        with self.client as client:

            response = client.get("/analytics", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Отправить ссылку для входа", html)
            self.assertEqual("form" in html, True)
            self.assertEqual("token" in session, False)

    def test_get_analytics_page_authorized(self):
        with self.client as client:

            with client.session_transaction() as session:
                session["token"] = True

            response = client.get("/analytics")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertEqual("table" in html, True)
            self.assertEqual("token" in session, True)

    def test_get_index_page_magic_link(self):
        user = User(email="test@gmail1.com")
        user.set_token()
        db.session.add(user)
        db.session.commit()

        with self.client as client:
            response = client.get(f"/{user.token}", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Вы прошли аутентификацию через email", html)
            self.assertEqual("form" in html, False)
            self.assertEqual("token" in session, True)

    def test_user_create(self):
        with mock.patch("mail.send_email") as mocked_send_email:
            with self.client as client:
                response = client.post(
                    f"/",
                    data=json.dumps({"email": "test@gmail.com"}),
                    content_type="application/json",
                    follow_redirects=True,
                )
                html = response.get_data(as_text=True)

                self.assertEqual(response.status_code, 200)
                self.assertTrue(mocked_send_email.called)
                self.assertIn("Сслылка для входа была отправлена на ваш email", html)
                self.assertEqual("form" in html, False)
                self.assertEqual("token" in session, False)


if __name__ == "__main__":
    unittest.main()
