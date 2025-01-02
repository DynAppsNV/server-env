import json

from odoo.tests import tagged

from odoo.addons.server_environment.tests.common import ServerEnvironmentCase


@tagged("post_install", "-at_install")
class TestMailEnvironment(ServerEnvironmentCase):
    def test_outgoing_mail_server(self):
        mail_server = (
            self.env["ir.mail_server"]
            .with_context(active_test=False)
            .search([("name", "=", "Test Outgoing Mail Server")])
        )
        self.assertTrue(mail_server)
        self.assertEqual(mail_server.smtp_host, "localhost")
        self.assertEqual(mail_server.smtp_port, 25)
        self.assertEqual(mail_server.smtp_user, "test")
        self.assertEqual(mail_server.smtp_pass, "test123")
        self.env.cr.execute(
            "SELECT * FROM ir_mail_server where name = 'Test Outgoing Mail Server'"
        )
        mail_server = self.env.cr.dictfetchone()
        server_env_defaults = json.loads(mail_server["server_env_defaults"])
        self.assertEqual(server_env_defaults["x_smtp_host_env_default"], "localhost")
        self.assertEqual(server_env_defaults["x_smtp_port_env_default"], 25)
        self.assertEqual(server_env_defaults["x_smtp_user_env_default"], "test")
        self.assertEqual(server_env_defaults["x_smtp_pass_env_default"], "test123")

    def test_incoming_mail_server(self):
        mail_server = (
            self.env["fetchmail.server"]
            .with_context(active_test=False)
            .search([("name", "=", "Test Incoming Mail Server")])
        )
        self.assertTrue(mail_server)
        self.assertEqual(mail_server.server, "localhost")
        self.assertEqual(mail_server.port, 143)
        self.assertEqual(mail_server.user, "test")
        self.assertEqual(mail_server.password, "test123")
        self.env.cr.execute(
            "SELECT * FROM fetchmail_server where name = 'Test Incoming Mail Server'"
        )
        mail_server = self.env.cr.dictfetchone()
        server_env_defaults = json.loads(mail_server["server_env_defaults"])
        self.assertEqual(server_env_defaults["x_server_env_default"], "localhost")
        self.assertEqual(server_env_defaults["x_port_env_default"], 143)
        self.assertEqual(server_env_defaults["x_user_env_default"], "test")
        self.assertEqual(server_env_defaults["x_password_env_default"], "test123")
