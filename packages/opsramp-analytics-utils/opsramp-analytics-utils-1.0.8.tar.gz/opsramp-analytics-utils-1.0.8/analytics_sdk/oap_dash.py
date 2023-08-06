import os
import json

import dash
import flask
import plotly
import pkgutil
import requests
import mimetypes
import dash_renderer
import dash_core_components as dcc

from dash.version import __version__
from dash import _validate
from dash._utils import (
    stringify_id,
    format_tag
)

from .utilities import (
    BASE_API_URL,
    call_get_requests
)

_app_entry = """
<div class="d-flex">
    <div class="sidebar d-print-none">
        <div id="root" class="h-100"></div>
    </div>
    <div class="analysis-content" style="flex: 1;">
        <div id="AnalyticsAppsUI-container">
            <div class="_dash-loading">
                Loading...
            </div>
        </div>
    </div>
</div>
"""

_re_index_entry_id_ = 'AnalyticsAppsUI-container'
_re_index_entry_id = f'id="{_re_index_entry_id_}"', f"#{_re_index_entry_id_}"

class OAPDash(dash.Dash):
    static_files = {
        'css': [
            # 'bootstrap.min.css',
            'main.wrapper.css'
        ],
        'js': [
            'main.wrapper.js'
        ]
    }

    def __init__(self, **kwargs):
        self.route = kwargs.pop('route')
        route_prefix = f'/{self.route}' if self.route else ''
        # assume this is not set by user
        kwargs['requests_pathname_prefix'] = f'{route_prefix}/'

        super(OAPDash, self).__init__(**kwargs)

    def init_app(self, app=None):
        """
        serve custom static files
        """
        super(OAPDash, self).init_app(app)

        # serve the wrapper's media
        assets_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'analysis-wrapper'
        )

        self.server.register_blueprint(
            flask.Blueprint(
                'analytics_sdk_assets',
                self.config.name,
                static_folder=assets_folder,
                static_url_path="{}{}".format(
                    self.config.routes_pathname_prefix,
                    'wrapper-static',
                )
            )
        )

        # register manifest file
        self._add_url("opsramp-analytics-utils/<string:file_name>", self.serve_resource)
        self._add_url("asset-manifest.json", self.serve_manifest)

    def is_authenticated(self):
        url = f'{BASE_API_URL}/api/v2/alertTypes'
        res = call_get_requests(url)

        return res.status_code == 200

    def _index(self, *args, **kwargs):  # pylint: disable=unused-argument
        scripts = self._generate_scripts_html()
        css = self._generate_css_dist_html()
        config = self._generate_config_html()
        metas = self._generate_meta_html()
        renderer = self._generate_renderer()

        # use self.title instead of app.config.title for backwards compatibility
        title = self.title

        if self._favicon:
            favicon_mod_time = os.path.getmtime(
                os.path.join(self.config.assets_folder, self._favicon)
            )
            favicon_url = self.get_asset_url(self._favicon) + "?m={}".format(
                favicon_mod_time
            )
        else:
            favicon_url = "{}_favicon.ico?v={}".format(
                self.config.requests_pathname_prefix, __version__
            )

        favicon = format_tag(
            "link",
            {"rel": "icon", "type": "image/x-icon", "href": favicon_url},
            opened=True,
        )

        index = self.interpolate_index(
            metas=metas,
            title=title,
            css=css,
            config=config,
            scripts=scripts,
            app_entry=_app_entry,
            favicon=favicon,
            renderer=renderer,
        )

        checks = (
            _re_index_entry_id,
        )
        _validate.validate_index("index", checks, index)
        return index

    def index(self, *args, **kwargs):  # pylint: disable=unused-argument
        index = self._index(args, kwargs)

        # check auth
        REQUIRE_AUTH_REDIRECT = os.getenv('REQUIRE_AUTH_REDIRECT') == 'true'
        if not REQUIRE_AUTH_REDIRECT or self.is_authenticated():
            return index
        else:
            PLATFORM_ROUTE = os.getenv("PLATFORM_ROUTE", '')
            redirect_url = f"/tenancy/web/login?cb=/{PLATFORM_ROUTE}"

            return flask.redirect(redirect_url, code=302)

    def serve_manifest(self):
        return {
            "files": {
                "main.css": "/analytics-apps/opsramp-analytics-utils/main.css",
                "main.js": "/analytics-apps/opsramp-analytics-utils/main.js",
                # "main.js.map": "/analytics-apps/static/js/main.b42d7633.js.map",
                "index.html": "/analytics-apps/index.html",
            },
            "entrypoints": [
                "main.css",
                "main.js"
            ]
        }

    def serve_resource(self, file_name):
        if file_name == 'main.css':
            return self._serve_main_css()
        elif file_name == 'main.js':
            return self._serve_main_js()
        else:
            extension = "." + file_name.split(".")[-1]
            mimetype = mimetypes.types_map.get(extension, "application/octet-stream")

            return flask.Response(
                pkgutil.get_data('dash_core_components', file_name), mimetype=mimetype
            )

    def _serve_main_css(self):
        body = ''

        # TODO: external css files using requests
        external_links = self.config.external_stylesheets

        # oap css files
        for file_path in self.static_files['css']:
            body += pkgutil.get_data('analytics_sdk', 'analysis-wrapper/'+file_path).decode("utf-8")
        body = body.replace('url(/static/media', f'url({self.config.requests_pathname_prefix}wrapper-static/media')

        # custom css files
        for resource in self.css.get_all_css():
            file_name = resource['asset_path']
            body += open(self.config.assets_folder+'/'+file_name).read()

        response = flask.Response(body, mimetype='text/css')

        return response

    def _serve_main_js(self):
        body = f"var oap_config = {json.dumps(self._config(), cls=plotly.utils.PlotlyJSONEncoder)};\n"

        # external js files
        external_links = self.config.external_scripts
        # urllib

        # inline scripts
        # self._inline_scripts

        # oap js files
        if os.getenv("INCLUDE_WRAPPER") == "true":
            for file_path in self.static_files['js']:
                body += pkgutil.get_data('analytics_sdk', 'analysis-wrapper/'+file_path).decode("utf-8")
            body = body.replace('static/media/', f'{self.config.requests_pathname_prefix.lstrip("/")}wrapper-static/media/')

        # system js files
        mode = "dev" if self._dev_tools["props_check"] is True else "prod"

        deps = []
        for js_dist_dependency in dash_renderer._js_dist_dependencies:
            dep = {}
            for key, value in js_dist_dependency.items():
                dep[key] = value[mode] if isinstance(value, dict) else value

            deps.append(dep)

        dev = self._dev_tools.serve_dev_bundles

        resources = (
            self.scripts._resources._filter_resources(deps, dev_bundles=dev)
          + self.scripts.get_all_scripts(dev_bundles=dev)
          + self.scripts._resources._filter_resources(dash_renderer._js_dist, dev_bundles=dev)
        )

        srcs = []
        for resource in resources:
            is_dynamic_resource = resource.get("dynamic", False)

            if "relative_package_path" in resource:
                paths = resource["relative_package_path"]
                paths = [paths] if isinstance(paths, str) else paths

                for rel_path in paths:
                    self.registered_paths[resource["namespace"]].add(rel_path)

                    if not is_dynamic_resource:
                        _body = pkgutil.get_data(resource["namespace"], rel_path).decode("utf-8")
                        body += self.pre_process(_body, rel_path, dev)
            # elif "external_url" in resource:
            #     if not is_dynamic_resource:
            #         if isinstance(resource["external_url"], str):
            #             srcs.append(resource["external_url"])
            #         else:
            #             srcs += resource["external_url"]
            # elif "asset_path" in resource:
            #     static_url = self.get_asset_url(resource["asset_path"])
            #     # Add a cache-busting query param
            #     srcs.append(static_url)

        body += "var renderer = new DashRenderer();"
        response = flask.Response(body, mimetype='application/javascript')

        return response

    def pre_process(self, txt_body, file_name, dev):
        if file_name.startswith('dash_renderer.'):
            txt_body = txt_body.replace("JSON.parse(document.getElementById('_dash-config').textContent);", "oap_config;")
            txt_body = txt_body.replace('react-entry-point', _re_index_entry_id_)

        return txt_body + "\n"

    def get_component_ids(self, layout):
        component_ids = []
        for component in layout._traverse():
            component_id = stringify_id(getattr(component, "id", None))
            component_ids.append(component_id)

        return component_ids

    def _layout_value(self):
        """
        add custom stores
        """
        _layout = self._layout() if self._layout_is_function else self._layout                        

        component_ids = self.get_component_ids(_layout)
        in_store_id = "_oap_data_in_" + self.route
        out_store_id = "_oap_data_out_" + self.route
        
        if in_store_id not in component_ids:
            _layout.children.append(dcc.Store(id="dummy-store"))
            _layout.children.append(dcc.Store(id=out_store_id, storage_type="local"))
            _layout.children.append(dcc.Store(id=in_store_id, storage_type="local"))
            _layout.children.append(dcc.Store(id='op-filter-start-date', storage_type="local"))
            _layout.children.append(dcc.Store(id='op-filter-end-date'))

        return _layout

    def _generate_renderer(self):
        return ''

    def _generate_config_html(self):
        return ''

    def _generate_css_dist_html(self):
        return f'<link rel="stylesheet" href="{self.config.requests_pathname_prefix}opsramp-analytics-utils/main.css">'

    def _generate_scripts_html(self):
        return f'<script src="{self.config.requests_pathname_prefix}opsramp-analytics-utils/main.js"></script>'
