# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020 Northwestern University.
# Copyright (C) 2021 TU Wien.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Bibliographic Record Resource."""

from flask import abort, g
from flask_resources import request_parser, resource_requestctx, \
    response_handler, route
from invenio_drafts_resources.resources import RecordResource
from invenio_drafts_resources.resources.records.errors import RedirectException
from invenio_records_resources.resources.records.resource import \
    request_data, request_search_args, request_view_args
from marshmallow_utils.fields import SanitizedUnicode


class RDMRecordResource(RecordResource):
    """RDM record resource."""


#
# Parent Record Links
#
class RDMParentRecordLinksResource(RecordResource):
    """Secret links resource."""

    def create_url_rules(self):
        """Create the URL rules for the record resource."""

        def p(route):
            """Prefix a route with the URL prefix."""
            return f"{self.config.url_prefix}{route}"

        routes = self.config.routes
        return [
            route("GET", p(routes["list"]), self.search),
            route("POST", p(routes["list"]), self.create),
            route("GET", p(routes["item"]), self.read),
            route("PUT", p(routes["item"]), self.update),
            route("PATCH", p(routes["item"]), self.partial_update),
            route("DELETE", p(routes["item"]), self.delete),
        ]

    @request_view_args
    @request_data
    @response_handler()
    def create(self):
        """Create a secret link for a record."""
        item = self.service.create_secret_link(
            id_=resource_requestctx.view_args["pid_value"],
            identity=g.identity,
            data=resource_requestctx.data,
        )

        return item.to_dict(), 201

    @request_view_args
    @response_handler()
    def read(self):
        """Read a secret link for a record."""
        item = self.service.read_secret_link(
            id_=resource_requestctx.view_args["pid_value"],
            identity=g.identity,
            link_id=resource_requestctx.view_args["link_id"],
        )
        return item.to_dict(), 200

    def update(self):
        """Update a secret link for a record."""
        abort(405)

    @request_view_args
    @request_data
    @response_handler()
    def partial_update(self):
        """Patch a secret link for a record."""
        item = self.service.update_secret_link(
            id_=resource_requestctx.view_args["pid_value"],
            identity=g.identity,
            link_id=resource_requestctx.view_args["link_id"],
            data=resource_requestctx.data,
        )
        return item.to_dict(), 200

    @request_view_args
    def delete(self):
        """Delete a a secret link for a record."""
        self.service.delete_secret_link(
            id_=resource_requestctx.view_args["pid_value"],
            identity=g.identity,
            link_id=resource_requestctx.view_args["link_id"],
        )
        return "", 204

    @request_search_args
    @request_view_args
    @response_handler(many=True)
    def search(self):
        """List secret links for a record."""
        items = self.service.read_secret_links(
            id_=resource_requestctx.view_args["pid_value"],
            identity=g.identity,
        )
        return items.to_dict(), 200


request_pid_args = request_parser(
    {"client": SanitizedUnicode()}, location='args'
)


class RDMManagedPIDProviderResource(RecordResource):
    """PID provider resource."""

    def create_url_rules(self):
        """Create the URL rules for the pid provider resource."""

        def p(route):
            """Prefix a route with the URL prefix."""
            return f"{self.config.url_prefix}{route}"

        routes = self.config.routes
        return [
            route("GET", p(routes["item"]), self.create),
            route("DELETE", p(routes["item"]), self.delete),
        ]

    @request_pid_args
    @request_view_args
    @request_data
    @response_handler()
    def create(self):
        """Reserve doi."""
        item = self.service.reserve_pid(
            id_=resource_requestctx.view_args["pid_value"],
            pid_type=resource_requestctx.view_args["pid_type"],
            pid_client=resource_requestctx.args.get("client"),
            identity=g.identity,
        )

        return item.to_dict(), 200

    @request_pid_args
    @request_view_args
    def delete(self):
        """Delete  doi."""
        self.service.delete_pid(
            id_=resource_requestctx.view_args["pid_value"],
            pid_type=resource_requestctx.view_args["pid_type"],
            pid_client=resource_requestctx.args.get("client"),
            identity=g.identity,
        )

        return "", 204


class PIDResolverResource(RecordResource):
    """PID resolver resource."""

    def create_url_rules(self):
        """Create the URL rules for the pid provider resource."""

        def p(route):
            """Prefix a route with the URL prefix."""
            return f"{self.config.url_prefix}{route}"

        routes = self.config.routes
        return [
            route("GET", p(routes["item-doi"]), self.read_doi),
            route("GET", p(routes["item"]), self.read),
        ]

    def _read(self, pid_value):
        """Read a record from a PID."""
        item = self.service.resolve_pid(
            id_=pid_value,
            pid_type=resource_requestctx.view_args["pid_type"],
            pid_client=resource_requestctx.args.get("client"),
            identity=g.identity,
        )

        return item

    @request_pid_args
    @request_view_args
    @response_handler()
    def read_doi(self):
        """Redirect to the record.

        GET /pids/:pid_type/:pid_prefix/:pid_value
        """
        pid_prefix = resource_requestctx.view_args["pid_prefix"]
        pid_value = resource_requestctx.view_args["pid_value"]
        if pid_prefix:
            pid_value = f"{pid_prefix}/{pid_value}"

        item = self._read(pid_value)

        raise RedirectException(item["links"]["self"])

    @request_pid_args
    @request_view_args
    @response_handler()
    def read(self):
        """Redirect to the record.

        GET /pids/:pid_type/:pid_value
        """
        item = self._read(resource_requestctx.view_args["pid_value"])

        raise RedirectException(item["links"]["self"])
