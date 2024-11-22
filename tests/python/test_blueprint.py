#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2021 TROUVERIE Joachim <jtrouverie@joakode.fr>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import unittest
from http import HTTPStatus

from flask import Blueprint, Flask

from flask_inertia import Inertia, render_inertia
from flask_inertia.unittest import InertiaTestResponse


class TestConfig:

    TESTING = True
    INERTIA_TEMPLATE = "base.html"


def index():
    return render_inertia("Index")


class TestBlueprint(unittest.TestCase):
    """Flask-Inertia blueprint tests."""

    def setUp(self):
        self.blueprint = Blueprint("inertia", __name__, template_folder=".")
        self.blueprint.add_url_rule("/", "index", index)

        self.inertia = Inertia(self.blueprint)
        self.inertia.add_shorthand_route("/faq/", "FAQ")

        self.app = Flask(__name__, template_folder=".")
        self.app.config.from_object(TestConfig)
        self.app.register_blueprint(self.blueprint)

        self.app.response_class = InertiaTestResponse
        self.client = self.app.test_client()

    def test_extension_registered(self):
        self.assertIn("inertia", self.app.extensions)

    def test_shorthand_route(self):
        response = self.client.get("/faq/")
        data = response.inertia("app")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(data.component, "FAQ")
