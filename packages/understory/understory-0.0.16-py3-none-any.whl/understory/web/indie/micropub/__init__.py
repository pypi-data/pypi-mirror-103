"""Micropub server app."""

import json
import pathlib

import sh
import vobject

from understory import web
from understory.web import tx

from .. import webmention


server = web.application("MicropubServer", mount_prefix="pub", db=False,
                         channel=r".+", entry=r".+", nickname=r"[a-z]+",
                         filename=rf"{web.nb60_re}{{4}}.\w{{1,10}}")
templates = web.templates(__name__)


def define_table():
    """Define the `resources`, `media` and `syndication` tables."""
    tx.db.define(resources="""url TEXT, resource JSON, modified DATETIME,
                              version TEXT UNIQUE, parents TEXT, alias TEXT""",
                 media="""mid TEXT, sha256 TEXT UNIQUE, size INTEGER""",
                 syndication="""destination JSON NOT NULL""")


def wrap_server(handler, app):
    """Ensure server links are in head of root document."""
    define_table()
    tx.pub = LocalClient()
    yield
    if tx.request.uri.path == "" and tx.response.body:
        doc = web.parse(tx.response.body)
        try:
            head = doc.select("head")[0]
        except IndexError:
            pass
        else:
            head.append("<link rel=micropub href=/pub>")
            tx.response.body = doc.html
        web.header("Link", '</pub>; rel="micropub"', add=True)


def discover_post_type(properties):
    """Return the discovered post type."""
    if "bookmark-of" in properties:
        post_type = "bookmark"
    elif "like-of" in properties:
        post_type = "like"
    elif "follow-of" in properties:
        post_type = "follow"
    elif "identification-of" in properties:
        post_type = "identification"
    elif "rsvp" in properties:
        post_type = "rsvp"
    elif "in-reply-to" in properties:
        post_type = "reply"
    elif "maintext" in properties:  # mj
        post_type = "poem"
    else:
        post_type = "note"
    return post_type


def send_request(payload):
    """Send a Micropub request to a Micropub server."""
    # TODO FIXME what's in the session?
    response = web.post(tx.user.session["micropub_endpoint"], json=payload)
    return response.location, response.links


def generate_vcard(nickname):
    """"""
    card = tx.pub.get_card(nickname)
    vcard = vobject.vCard()
    vcard.add("prodid").value = "-//Canopy//understory 0.0.0//EN"
    vcard.add("uid").value = card["uid"][0]
    vcard.add("fn").value = card["name"][0]
    return vcard.serialize()

    # TODO # TODO if identity["type"] == "identity":
    # TODO n = card.add("n")
    # TODO names = {}
    # TODO for name_type in ("prefix", "given", "additional",
    #                        "family", "suffix"):
    # TODO     if identity[name_type]:
    # TODO         names[name_type] = identity[name_type].split(";")
    # TODO n.value = vobject.vcard.Name(**names)
    # TODO # TODO else:
    # TODO # TODO     card.add("n")
    # TODO # TODO     card.add("org").value = [identity["name"]]

    # TODO # TODO card.add("nickname").value = identity["name"]
    # TODO card.add("sort_string").value = identity["sort_string"]

    # TODO for number, types in identity["telephones"]:
    # TODO     entry = card.add("tel")
    # TODO     entry.value = number
    # TODO     if types:
    # TODO         entry.params["TYPE"] = types

    # TODO for url, types in identity["websites"]:
    # TODO     entry = card.add("url")
    # TODO     entry.value = url
    # TODO     if types:
    # TODO         entry.params["TYPE"] = types

    # TODO try:
    # TODO     photo_id = identity["photos"][0]
    # TODO except IndexError:
    # TODO     pass
    # TODO else:
    # TODO     photo_data = \
    # TODO         canopy.branches["images"].photos.get_photo_data(id=photo_id)
    # TODO     photo = card.add("photo")
    # TODO     photo.value = photo_data
    # TODO     photo.encoding_param = "b"
    # TODO     photo.type_param = "JPEG"

    # item_index = 0
    # for vals in card.contents.values():
    #     for val in vals:
    #         if val.group:
    #             item_index = int(val.group[4:])

    # for related, types in get_relationships(identity["id"]):
    #     uri = "https://{}/identities/{}/{}.vcf".format(tx.host.name,
    #                                                related["identifier"],
    #                                                related["slug"])
    #     rel = card.add("related")
    #     rel.value = uri
    #     rel.params["TYPE"] = types
    #     for type in types:
    #         group_name = "item{}".format(item_index)
    #         rel_name = card.add("x-abrelatednames")
    #         rel_name.value = related["name"]
    #         rel_name.group = group_name
    #         rel_uri = card.add("x-aburi")
    #         rel_uri.value = uri
    #         rel_uri.group = group_name
    #         rel_type = card.add("x-ablabel")
    #         rel_type.value = "_$!<{}>!$_".format(type)
    #         rel_type.group = group_name
    #         item_index += 1


class LocalClient:
    """A localized interface to the endpoint's backend."""

    def create(self, resource_type, **resource):
        """Create a resource and return its permalink."""
        for k, v in resource.items():
            if not isinstance(v, list):
                resource[k] = [v]
        published = resource.get("published", [web.utcnow()])
        visibility = resource.get("visibility", ["public"])
        channels = resource.get("channel", ["default"])
        path = "/"
        mentions = []
        if resource_type == "card":
            slug = resource.get("nickname", resource.get("name"))[0]
            path += f"people/{web.textslug(slug)}"
            # if resource["uid"] == str(web.uri(tx.host.name)):
            #     pass
        elif resource_type == "event":
            slug = resource.get("nickname", resource.get("name"))[0]
            path += f"people/{web.textslug(slug)}"
            # if resource["uid"] == str(web.uri(tx.host.name)):
            #     pass
        elif resource_type == "entry":
            post_type = discover_post_type(resource)
            timeslug = web.timeslug(published[0])
            if post_type == "note":
                textslug = resource["content"][0]
            elif post_type == "bookmark":
                bookmarks = resource["bookmark-of"]
                bookmarks[0] = {"type": "cite", **bookmarks[0]["properties"]}
                textslug = bookmarks[0]["name"]
                mentions.append(bookmarks[0]["url"])
            elif post_type == "like":
                likes = resource["like-of"]
                likes[0] = {"type": "cite", **likes[0]["properties"]}
                textslug = likes[0]["name"]
                mentions.append(likes[0]["url"])
            elif post_type == "identification":
                identifications = resource["identification-of"]
                identifications[0] = {"type": "cite",
                                      **identifications[0]["properties"]}
                textslug = identifications[0]["name"]
                mentions.append(identifications[0]["url"])
            elif post_type == "follow":
                follows = resource["follow-of"]
                follows[0] = {"type": "cite", **follows[0]["properties"]}
                textslug = follows[0]["name"]
                mentions.append(follows[0]["url"])
                tx.sub.follow(follows[0]["url"])
            elif post_type == "rsvp":
                events = resource["in-reply-to"]
                events[0] = {"type": "cite", **events[0]["properties"]}
                textslug = events[0]["name"]
                mentions.append(events[0]["url"])
            elif post_type == "poem":
                # poem = resource["in-reply-to"]
                # events[0] = {"type": "cite", **events[0]["properties"]}
                textslug = resource["name"]
                # mentions.append(events[0]["url"])
            path += f"{timeslug}/{web.textslug(textslug)}"
            author_id = tx.db.select("resources", where="url = ?",
                                     vals=["/people/me"],
                                     order="modified DESC")[0]["version"]
            resource.update(published=published,
                            url=[path], author=[author_id])
        elif resource_type == "room":
            print("MAKING A ROOM")
            pass
        resource["type"] = [resource_type]
        resource["visibility"] = visibility
        resource["channel"] = channels
        resource_kwargs = dict(url=path, modified=published[0],
                               resource=resource, version=web.nbrandom(10))
        from pprint import pprint
        pprint(resource_kwargs)
        if "alias" in resource:
            resource_kwargs["alias"] = resource.pop('alias')
        # XXX resource["alias"] = resource["name"]
        tx.db.insert("resources", **resource_kwargs)
        web.publish("/recent", ".feed[-0:-0]", resource)
        for mention in mentions:
            web.enqueue(webmention.send, f"{tx.origin}{path}", mention)
            # TODO web.publish(mention, ".responses[-1:-1]", resource)
        return path

    def update(self, url, add=None, replace=None, delete=None):
        """Update a resource."""
        now = web.utcnow()
        url = f"/{url.strip('/')}"
        if add:
            for prop, vals in add.items():
                # TODO abstract JSON loading/dumping
                v = tx.db.select("resources",
                                 what=f"""json_extract(resources.resource,
                                              '$.{prop}') as vals""",
                                 where="url = ?", vals=[url])[0]["vals"]
                v = json.loads(v)
                v.extend(vals)
                v = json.dumps(v)
                tx.db.update("resources",
                             what=f"""resource = json_set(resources.resource,
                                          '$.{prop}', json('{v}')),
                                      modified = ?, version = ?""",
                             where="url = ?", vals=[now, web.nbrandom(10),
                                                    url])
                web.publish(url, f".{prop}[-0:-0]", vals)

    def delete(self, url):
        """Delete a resource."""
        pass  # TODO

    def search(self, query):
        """Return a list of resources containing `query`."""
        where = """json_extract(resources.resource,
                       '$.bookmark-of[0].url') == ?
                   OR json_extract(resources.resource,
                       '$.like-of[0].url') == ?"""
        return tx.db.select("resources", vals=[query, query], where=where)

    def read(self, url):
        """Return an entry with its metadata."""
        url = f"/{url.rstrip('/')}"
        try:
            resource = tx.db.select("resources", where="url = ?",
                                    vals=[url])[0]
        except IndexError:
            resource = tx.db.select("resources", where="alias = ?",
                                    vals=[url])[0]
        r = resource["resource"]
        if "entry" in r["type"]:
            r["author"] = self.get_version(r["author"][0])["resource"]
        return resource

    def get_version(self, version):
        """Return a snapshot of resource at given version."""
        return tx.db.select("resources", where="version = ?",
                            vals=[version])[0]

    def get_entry(self, path):
        """"""

    def get_card(self, nickname):
        """Return the card with given nickname."""
        resource = tx.db.select("resources", vals=[nickname],
                                where="""json_extract(resources.resource,
                                         '$.nickname[0]') == ?""")[0]
        return resource["resource"]

    def get_event(self, path):
        """"""

    def get_entries(self, limit=20, modified="DESC"):
        """Return a list of entries."""
        return tx.db.select("resources", order=f"modified {modified}",
                            where="""json_extract(resources.resource,
                                         '$.type[0]') == 'entry'""",
                            limit=limit)

    def get_cards(self, limit=20):
        """Return a list of alphabetical cards."""
        return tx.db.select("resources", order="modified DESC",
                            where="""json_extract(resources.resource,
                                         '$.type[0]') == 'card'""")

    def get_channels(self):
        """Return a list of channels."""
        return [r["value"] for r in
                tx.db.select("""resources,
                                json_tree(resources.resource, '$.channel')""",
                             what="DISTINCT value", where="type = 'text'")]

    def get_media(self):
        """Return a list of media filepaths."""
        try:
            filepaths = list(pathlib.Path(tx.host.name).iterdir())
        except FileNotFoundError:
            filepaths = []
        return filepaths

    def get_filepath(self, filename):
        """Return a media file's path."""
        return pathlib.Path(tx.host.name) / filename


@server.route(r"")
class MicropubEndpoint:
    """."""

    def _get(self):
        try:
            form = web.form("q")
        except web.BadRequest:
            local_client = LocalClient()
            channels = local_client.get_channels()
            entries = local_client.get_entries()
            cards = local_client.get_cards()
            media = local_client.get_media()
            return templates.activity(channels, entries, cards, media)
        syndication_endpoints = []
        if form.q == "config":
            response = {"q": ["category", "contact", "source", "syndicate-to"],
                        "media-endpoint": f"https://{tx.host.name}/pub/media",
                        "syndicate-to": syndication_endpoints,
                        "visibility": ["public", "unlisted", "private"]}
        elif form.q == "source":
            response = {}
            if "search" in form:
                response = {"items": [{"url": [r["resource"]["url"]]} for r in
                                      LocalClient().search(form.search)]}
            if "url" in form:
                response = dict(LocalClient().read(form.url))
        else:
            raise web.BadRequest("""unsupported query.
                                    check `q=config` for support.""")
        web.header("Content-Type", "application/json")
        return response

    def _post(self):
        try:
            form = web.form("h")
        except web.BadRequest:
            resource = tx.request.body._data
        else:
            h = form.pop('h')
            properties = {k.rstrip("[]"): (v if isinstance(v, list) else [v])
                          for k, v in form.items()}
            resource = {"type": [f"h-{h}"], "properties": properties}
        client = LocalClient()
        action = resource.pop("action", None)
        if action == "update":
            url = resource.pop("url")
            client.update(url, **resource)
            return
        permalink = client.create(resource["type"][0].partition("-")[2],
                                  **resource["properties"])
        # web.header("Link", '</blat>; rel="shortlink"', add=True)
        # web.header("Link", '<https://twitter.com/angelogladding/status/'
        #                    '30493490238590234>; rel="syndication"', add=True)
        raise web.Created("post created", permalink)


@server.route(r"channels")
class Channels:
    """All channels."""

    def _get(self):
        return templates.channels(LocalClient().get_channels())


@server.route(r"channels/{channel}")
class Channel:
    """A single channel."""

    def _get(self):
        return templates.channel(self.channel)


@server.route(r"entries")
class Entries:
    """All entries on file."""

    def _get(self):
        return templates.entries(LocalClient().get_entries())


@server.route(r"entries/{entry}")
class Entry:
    """A single entry on file."""

    def _get(self):
        try:
            resource = tx.db.select("cache", where="url = ?",
                                    vals=[f"https://{self.resource}"])[0]
        except IndexError:
            resource = tx.db.select("cache", where="url = ?",
                                    vals=[f"http://{self.resource}"])[0]
        return templates.cache_resource(resource)


@server.route(r"cards")
class Cards:
    """
    All cards on file.

    `OPTIONS`, `PROPFIND` and `REPORT` methods provide CardDAV support.

    """

    def _get(self):
        return templates.cards(tx.pub.get_cards())

    def _options(self):
        """Signal capabilities to CardDAV client."""
        web.header("DAV", "1, 2, 3, access-control, addressbook")
        web.header("Allow", "OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, "
                            "COPY, MOVE, MKCOL, PROPFIND, PROPPATCH, LOCK, "
                            "UNLOCK, REPORT, ACL")
        tx.response.naked = True
        return ""

    def _propfind(self):
        """
        Return a status listing of addressbook/contacts.

        This resource is requsted twice with `Depth` headers of 0 and 1.
        0 is a request for the addressbook itself. 1 is a request for the
        addressbook itself and all contacts in the addressbook. Thus both
        the addressbook itself and each user have an etag.

        """
        # TODO refactor..
        web.header("DAV", "1, 2, 3, access-control, addressbook")

        depth = int(tx.request.headers["Depth"])
        etags = {"": tx.kv["carddav-lasttouch"]}
        if depth == 1:
            for identity in get_resources("identities"):
                etags[identity["-uuid"]] = \
                    identity.get("updated", identity["published"]).timestamp()

        props = list(tx.request.body.iterchildren())[0]
        namespaces = set()
        responses = []

        for uuid, etag in etags.items():
            ok = []
            notfound = []
            for prop in props.iterchildren():
                # supported
                if prop.tag == "{DAV:}current-user-privilege-set":
                    ok.append("""<current-user-privilege-set>
                                     <privilege>
                                         <all />
                                         <read />
                                         <write />
                                         <write-properties />
                                         <write-content />
                                     </privilege>
                                 </current-user-privilege-set>""")
                if prop.tag == "{DAV:}displayname":
                    ok.append("<displayname>carddav</displayname>")
                if prop.tag == "{DAV:}getetag":
                    ok.append(f'<getetag>"{etag}"</getetag>')
                if prop.tag == "{DAV:}owner":
                    ok.append("<owner>/</owner>")
                if prop.tag == "{DAV:}principal-URL":
                    ok.append("""<principal-URL>
                                     <href>/identities</href>
                                 </principal-URL>""")
                if prop.tag == "{DAV:}principal-collection-set":
                    ok.append("""<principal-collection-set>
                                     <href>/identities</href>
                                 </principal-collection-set>""")
                if prop.tag == "{DAV:}current-user-principal":
                    ok.append("""<current-user-principal>
                                     <href>/identities</href>
                                 </current-user-principal>""")
                if prop.tag == "{DAV:}resourcetype":
                    namespaces.add("CR")
                    if uuid:
                        ok.append("<resourcetype />")
                    else:
                        ok.append("""<resourcetype>
                                         <CR:addressbook />
                                         <collection />
                                     </resourcetype>""")
                if prop.tag == "{DAV:}supported-report-set":
                    ok.append("""<supported-report-set>
                                     <supported-report>
                                         <report>principal-property-search</report>
                                     </supported-report>
                                     <supported-report>
                                         <report>sync-collection</report>
                                     </supported-report>
                                     <supported-report>
                                         <report>expand-property</report>
                                     </supported-report>
                                     <supported-report>
                                         <report>principal-search-property-set</report>
                                     </supported-report>
                                 </supported-report-set>""")
                if (prop.tag == "{urn:ietf:params:xml:ns:carddav}"
                                "addressbook-home-set"):
                    namespaces.add("CR")
                    ok.append("""<CR:addressbook-home-set>
                                     <href>/identities</href>
                                 </CR:addressbook-home-set>""")
                if (prop.tag == "{http://calendarserver.org/ns/}"
                                "getctag"):
                    namespaces.add("CS")
                    ok.append(f'<CS:getctag>"{etag}"</CS:getctag>')

                # conditionally supported
                if (prop.tag == "{http://calendarserver.org/ns/}me-card"):
                    namespaces.add("CS")
                    if uuid:
                        notfound.append("<CS:me-card />")
                    else:
                        ok.append(f"""<CS:me-card>
                                      <href>/identities/{tx.owner["-uuid"]}.vcf</href>
                                      </CS:me-card>""")

                # not supported
                if prop.tag == "{DAV:}add-member":
                    notfound.append("<add-member />")
                if prop.tag == "{DAV:}quota-available-bytes":
                    notfound.append("<quota-available-bytes />")
                if prop.tag == "{DAV:}quota-used-bytes":
                    notfound.append("<quota-used-bytes />")
                if prop.tag == "{DAV:}resource-id":
                    notfound.append("<resource-id />")
                if prop.tag == "{DAV:}sync-token":
                    notfound.append("<sync-token />")
                if (prop.tag == "{urn:ietf:params:xml:ns:carddav}"
                                "directory-gateway"):
                    namespaces.add("CR")
                    notfound.append("<CR:directory-gateway />")
                if (prop.tag == "{urn:ietf:params:xml:ns:carddav}"
                                "max-image-size"):
                    namespaces.add("CR")
                    notfound.append("<CR:max-image-size />")
                if (prop.tag == "{urn:ietf:params:xml:ns:carddav}"
                                "max-resource-size"):
                    namespaces.add("CR")
                    notfound.append("<CR:max-resource-size />")
                if (prop.tag == "{http://calendarserver.org/ns/}"
                                "email-address-set"):
                    namespaces.add("CS")
                    notfound.append("<CS:email-address-set />")
                if (prop.tag == "{http://calendarserver.org/ns/}"
                                "push-transports"):
                    namespaces.add("CS")
                    notfound.append("<CS:push-transports />")
                if (prop.tag == "{http://calendarserver.org/ns/}"
                                "pushkey"):
                    namespaces.add("CS")
                    notfound.append("<CS:pushkey />")
                if (prop.tag == "{http://me.com/_namespace/}"
                                "bulk-requests"):
                    namespaces.add("ME")
                    notfound.append("<ME:bulk-requests />")
            href = "/identities"
            if uuid:
                href += f"/{uuid}.vcf"
            responses.append((href, ok, notfound))
        tx.response.naked = True
        raise web.MultiStatus(view.carddav(namespaces, responses))

    def _report(self):
        """Return a full listing for each requested identity."""
        etags = {}
        for identity in get_resources("identities"):
            etags[identity["-uuid"]] = \
                identity.get("updated", identity["published"]).timestamp()
        children = list(tx.request.body.iterchildren())
        # XXX props = children[0]  # TODO soft-code prop responses
        responses = []
        for href in children[1:]:
            uuid = href.text.rpartition("/")[2].partition(".")[0]
            ok = [f'<getetag>"{etags[uuid]}"</getetag>',
                  f"<CR:address-data>{generate_vcard(uuid)}</CR:address-data>"]
            notfound = []
            responses.append((href.text, ok, notfound))
        tx.response.naked = True
        raise web.MultiStatus(view.carddav(set(["CR"]), responses))


@server.route(r"cards/{nickname}")
class Card:
    """A single card on file."""

    def _get(self):
        # try:
        #     resource = tx.db.select("cache", where="url = ?",
        #                             vals=[f"https://{self.resource}"])[0]
        # except IndexError:
        #     resource = tx.db.select("cache", where="url = ?",
        #                             vals=[f"http://{self.resource}"])[0]
        return templates.card(tx.pub.get_card(self.nickname))


@server.route(r"cards/{nickname}.vcf")
class VCard:
    """
    A single card on file, represented as a vCard.
    
    `PUT` and `DELETE` methods provide CardDAV support.

    """

    def _get(self):
        web.header("Content-Type", "text/vcard")
        return generate_vcard(self.nickname)

    def _put(self):
        """
        add or update a identity

        """
        # TODO only add if "if-none-match" is found and identity isn't
        try:
            print("if-none-match", tx.request.headers.if_none_match)
        except AttributeError:
            pass
        else:
            try:
                identities.get_identity_by_uuid(self.card_id)
            except ResourceNotFound:
                pass
            else:
                raise web.Conflict("identity already exists")

        # TODO only update if "if-match" matches etag on hand
        try:
            request_etag = str(tx.request.headers.if_match).strip('"')
            print("if-match", request_etag)
        except AttributeError:
            pass
        else:
            identity = identities.get_identity_by_uuid(self.card_id)
            current_etag = \
                identity.get("updated", identity["published"]).timestamp()
            print("current etag", current_etag)
            if request_etag != current_etag:
                raise web.Conflict("previous edit already exists")

        # TODO non-standard type-params (url) not handled by vobject

        card = vobject.readOne(tx.request.body.decode("utf-8"))

        name = card.fn.value.strip()

        extended = {}
        n = card.n.value

        def explode(key):
            item = getattr(n, key)
            if isinstance(item, list):
                extended[key] = ";".join(item)
            else:
                extended[key] = [item]
        explode("prefix")
        explode("given")
        explode("additional")
        explode("family")
        explode("suffix")

        # TODO identity_type = "identity"
        basic = {"name": name, "uuid": self.card_id}

        # TODO organizations = [o.value[0]
        # TODO                  for o in card.contents.get("org", [])]
        # TODO for organization in organizations:
        # TODO     if organization == name:
        # TODO         identity_type = "organization"

        # TODO telephones = []
        # TODO for tel in card.contents.get("tel", []):
        # TODO     telephones.append((tel.value, tel.params["TYPE"]))
        # TODO websites = []
        # TODO for url in card.contents.get("url", []):
        # TODO     type = url.params.get("TYPE", [])
        # TODO     for label in card.contents.get("x-ablabel"):
        # TODO         if label.group == url.group:
        # TODO             type.append(label.value)
        # TODO     print(url.value, type)
        # TODO     print()
        # TODO     websites.append((url.value, type))

        # photo = card.contents.get("photo")[0]
        # print()
        # print(photo)
        # print()
        # print(photo.group)
        # print(photo.params.get("ENCODING"))
        # print(photo.params.get("X-ABCROP-RECTANGLE"))
        # print(photo.params.get("TYPE", []))
        # print(len(photo.value))
        # print()
        # filepath = tempfile.mkstemp()[1]
        # with open(filepath, "wb") as fp:
        #     fp.write(photo.value)
        # photo_id = canopy.branches["images"].photos.upload(filepath)
        # extended["photos"] = [photo_id]

        try:
            details = identities.get_identity_by_uuid(self.card_id)
        except ResourceNotFound:
            print("NEW identity!")
            print(basic)
            print(extended)
            quick_draft("identity", basic,
                        publish="Identity imported from iPhone.")
            # XXX details = create_identity(access="private", uid=self.card_id,
            # XXX                          **basic)
            # XXX details = update_identity(identifier=details["identifier"],
            # XXX                  telephones=telephones, websites=websites,
            # XXX                  **extended)
            print("CREATED")
        else:
            print("EXISTING identity!")
            print(details)
            print("UPDATED")
        # XXX     basic.update(extended)
        # XXX     details = update_identity(identifier=details["identifier"],
        # XXX                      telephones=telephones, websites=websites,
        # XXX                      **basic)
        identity = identities.get_identity_by_uuid(self.card_id)
        etag = identity.get("updated", identity["published"]).timestamp()
        web.header("ETag", f'"{etag}"')
        tx.response.naked = True
        raise web.Created("created identity",
                          f"/identities/{self.card_id}.vcf")

    def _delete(self):
        """
        delete a identity

        This method provides CardDAV support.

        """
        # delete_resource(...)
        tx.response.naked = True
        return f"""<?xml version="1.0"?>
                   <multistatus xmlns="DAV:">
                     <response>
                       <href>/identities/{self.card_id}.vcf</href>
                       <status>HTTP/1.1 200 OK</status>
                     </response>
                   </multistatus>"""


@server.route(r"syndication")
class Syndication:
    """."""

    def _get(self):
        return templates.syndication()

    def _post(self):
        destinations = web.form()
        if "twitter_username" in destinations:
            un = destinations.twitter_username
            # TODO pw = destinations.twitter_password
            # TODO sign in
            user_photo = ""  # TODO doc.qS(f"a[href=/{un}/photo] img").src
            destination = {"uid": f"//twitter.com/{un}",
                           "name": f"{un} on Twitter",
                           "service": {"name": "Twitter",
                                       "url": "//twitter.com",
                                       "photo": "//abs.twimg.com/favicons/"
                                                "twitter.ico"},
                           "user": {"name": un, "url": f"//twitter.com/{un}",
                                    "photo": user_photo}}
            tx.db.insert("syndication", destination=destination)
        if "github_username" in destinations:
            un = destinations.github_username
            # TODO token = destinations.github_token
            # TODO check the token
            user_photo = ""  # TODO doc.qS("img.avatar-user.width-full").src
            destination = {"uid": f"//github.com/{un}",
                           "name": f"{un} on GitHub",
                           "service": {"name": "GitHub",
                                       "url": "//github.com",
                                       "photo": "//github.githubassets.com/"
                                                "favicons/favicon.png"},
                           "user": {"name": un, "url": f"//github.com/{un}",
                                    "photo": user_photo}}
            tx.db.insert("syndication", destination=destination)


@server.route(r"media")
class MediaEndpoint:
    """."""

    def _get(self):
        return templates.media(LocalClient().get_media())

    def _post(self):
        media_dir = pathlib.Path(tx.host.name)
        media_dir.mkdir(exist_ok=True, parents=True)
        while True:
            mid = web.nbrandom(4)
            filename = media_dir / mid
            if not filename.exists():
                filename = web.form("file").file.save(filename)
                break
        if str(filename).endswith(".heic"):
            sh.convert(filename, "-set", "filename:base", "%[basename]",
                       f"{media_dir}/%[filename:base].jpg")
        sha256 = str(sh.sha256sum(filename)).split()[0]
        try:
            tx.db.insert("media", mid=mid, sha256=sha256,
                         size=filename.stat().st_size)
        except tx.db.IntegrityError:
            mid = tx.db.select("media", where="sha256 = ?",
                               vals=[sha256])[0]["mid"]
            filename.unlink()
        path = f"/pub/media/{mid}"
        raise web.Created(f"File can be found at <a href={path}>{path}</a>",
                          location=path)


@server.route(r"media/{filename}")
class MediaFile:
    """."""

    def _get(self):
        content_types = {(".jpg", ".jpeg"): "image/jpg",
                         ".heic": "image/heic",
                         ".png": "image/png",
                         ".mp3": "audio/mpeg",
                         ".mov": "video/quicktime",
                         ".mp4": "video/mp4"}
        for suffix, content_type in content_types.items():
            if self.filename.endswith(suffix):
                web.header("Content-Type", content_type)
                break
        relative_path = f"{tx.host.name}/{self.filename}"
        if tx.host.server[0] == "gunicorn":
            with open(relative_path, "rb") as fp:
                return fp.read()
        else:  # assumes Nginx context
            web.header("X-Accel-Redirect", f"/X/{relative_path}")

    def _delete(self):
        filepath = LocalClient().get_filepath(self.filename)
        tx.db.delete("media", where="mid = ?", vals=[filepath.stem])
        filepath.unlink()
        return "deleted"
