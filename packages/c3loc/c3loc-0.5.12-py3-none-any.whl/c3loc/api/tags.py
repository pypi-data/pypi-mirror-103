from datetime import datetime
import json

from aiohttp import web
from aiohttp_cors import CorsViewMixin
import asyncpg
from dateutil.parser import isoparse
from marshmallow import EXCLUDE
import pytz

from .schemas import (ibeacon_post_schema, macbeacon_post_schema, tag_patch_schema,
                      history_schema, secure_beacon_post_schema, contacts_schema)
from .views import ValidatingView, paginate_query


def tag_schema_dump(row):
    if row['type'] in {'iBeacon', 'LocationAnchor'}:
        return ibeacon_post_schema.dump(row)
    if row['type'] in {'SecureLocationAnchor', 'SecureSmartRelay'}:
        return secure_beacon_post_schema.dump(row)
    return macbeacon_post_schema.dump(row)


class TagsView(ValidatingView):
    async def get(self):
        async with self.request.app['db_pool'].acquire() as conn:
            query = None
            if 'type' in self.request.query:
                query = ('SELECT * from tags WHERE type = $1',
                         self.request.query['type'])
            elif 'group_id' in self.request.query:
                try:
                    query = ('SELECT * from tags WHERE group_id = $1',
                             int(self.request.query['group_id']))
                except ValueError:
                    raise web.HTTPBadRequest(text='bad group_id')
            else:
                query = ('SELECT * from tags', )
            query = paginate_query(self.request, query)
            try:
                tags = await conn.fetch(*query)
            except asyncpg.exceptions.InvalidTextRepresentationError:
                raise web.HTTPBadRequest(text='Invalid tag type')
            return web.json_response([tag_schema_dump(r) for r in tags if r is not None])

    async def post(self):
        body = await self._valid_json(self.request)

        if 'type' not in body:
            raise web.HTTPBadRequest(reason='Type field is required for post')

        new_t = {}
        if body['type'] in {'iBeacon', 'LocationAnchor'}:
            new_t.update(self._validate(ibeacon_post_schema, body))
        elif body['type'] == 'SmartRelay':
            new_t.update(self._validate(macbeacon_post_schema, body))
        elif body['type'] in {'SecureSmartRelay', 'SecureLocationAnchor'}:
            new_t.update(self._validate(secure_beacon_post_schema, body))
        else:
            raise web.HTTPBadRequest(reason=f'Unknown tag type {body["type"]}')

        async with self.request.app['db_pool'].acquire() as conn:
            try:
                await conn.execute('INSERT INTO tags (mac, uuid, major, minor, type, zone_id, name, group_id, bid, attrs) VALUES '
                                   '($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)',
                                   new_t.get('mac', None),
                                   new_t.get('uuid', None),
                                   new_t.get('major', None),
                                   new_t.get('minor', None),
                                   new_t['type'],
                                   new_t.get('zone_id', None),
                                   new_t.get('name', None),
                                   new_t.get('group_id', None),
                                   new_t.get('bid', None),
                                   json.dumps(new_t.get('attrs', {})))
            except asyncpg.exceptions.UniqueViolationError as e:
                raise web.HTTPConflict(reason=str(e.detail))
            except (asyncpg.exceptions.InvalidTextRepresentationError,
                    asyncpg.exceptions.NotNullViolationError,
                    asyncpg.exceptions.ForeignKeyViolationError) as e:
                raise web.HTTPBadRequest(reason=str(e.detail))
        raise web.HTTPCreated


def parse_start_end(request):
    utc = pytz.timezone('UTC')
    if 'start' in request.query:
        try:
            start = isoparse(request.query['start'])
        except ValueError:
            raise web.HTTPBadRequest(reason="Invailid ISO8601 in start parameter")
        if start.tzinfo:
            start = start.astimezone(utc).replace(tzinfo=None)
    else:
        start = datetime.min
    if 'end' in request.query:
        try:
            end = isoparse(request.query['end'])
        except ValueError:
            raise web.HTTPBadRequest(reason="Invailid ISO8601 in end parameter")
        if end.tzinfo:
            end = end.astimezone(utc).replace(tzinfo=None)
    else:
        end = datetime.max
    return start, end


class TagHistoryView(web.View, CorsViewMixin):
    async def get(self):
        t_id = int(self.request.match_info['id'])
        start, end = parse_start_end(self.request)
        async with self.request.app['db_pool'].acquire() as conn:
            query = (
            """SELECT tag_id,
       zone_id,
       start_ts,
       distance,
       coalesce(end_ts, (now() at time zone 'utc'))            as end_ts,
       coalesce(end_ts, (now() at time zone 'utc')) - start_ts as duration
FROM history
WHERE tag_id = $1 AND start_ts >= $2 AND coalesce(end_ts, (now() at time zone 'utc')) <= $3
ORDER BY start_ts DESC""", t_id, start, end)
            query = paginate_query(self.request, query)
            history = await conn.fetch(*query)
            return web.json_response(history_schema.dump(history))


class TagContactView(web.View, CorsViewMixin):
    async def get(self):
        t_id = int(self.request.match_info['id'])
        start, end = parse_start_end(self.request)
        async with self.request.app['db_pool'].acquire() as conn:
            query = (
                """SELECT tag_id, tags.name, start_ts, end_ts, end_ts - start_ts as duration, b.zone_id, zone_name
FROM (
         WITH cte as (
             SELECT tag_id, start_ts, coalesce(end_ts, (now() at time zone 'utc')) as end_ts
             FROM history
             WHERE tag_id = $1 AND start_ts >= $2 AND end_ts <= $3
         )
         SELECT history.tag_id                                                          as tag_id,
                greatest(history.start_ts, cte.start_ts)                                as start_ts,
                least(coalesce(history.end_ts, (now() at time zone 'utc')), cte.end_ts) as end_ts,
                zone_id,
                zone_name
         FROM history,
              cte
         WHERE history.start_ts >= $2 AND history.end_ts <= $3 AND (cte.start_ts, cte.end_ts) OVERLAPS (history.start_ts, history.end_ts)
           AND history.tag_id != $1
     ) b JOIN tags on tags.id = tag_id""", t_id, start, end)
            query = paginate_query(self.request, query)
            contacts = await conn.fetch(*query)
            return web.json_response(contacts_schema.dump(contacts))


class TagView(ValidatingView):
    async def get(self):
        t_id = int(self.request.match_info['id'])
        async with self.request.app['db_pool'].acquire() as conn:
            l = await conn.fetchrow('SELECT * FROM tags t WHERE id = $1', t_id)
            if not l:
                raise web.HTTPNotFound
            return web.json_response(tag_schema_dump(l))

    async def patch(self):
        t_id = int(self.request.match_info['id'])
        async with self.request.app['db_pool'].acquire() as conn:
            row = await conn.fetchrow('SELECT * FROM tags t WHERE id = $1', t_id)
            if not row:
                raise web.HTTPNotFound
            tag = dict(row.items())
            body = await self._valid_json(self.request)
            updates = self._validate(tag_patch_schema, body)
            if 'type' in updates:
                del body['type']  # Ensure that we are validating against existing type
            tag.update(updates)
            if tag['type'] in {'iBeacon', 'LocationAnchor'}:
                self._validate(ibeacon_post_schema, tag, unknown=EXCLUDE)
            elif tag['type'] == 'SmartRelay':
                self._validate(macbeacon_post_schema, tag, unknown=EXCLUDE)
            elif tag['type'] in {'SecureSmartRelay', 'SecureLocationAnchor'}:
                self._validate(secure_beacon_post_schema, tag, unknown=EXCLUDE)
            else:
                raise web.HTTPBadRequest(reason=f'Unknown tag type {body["type"]}')
            await conn.execute('UPDATE tags SET name = $1, mac = $2, uuid = $3, major = $4, '
                               'minor = $5, attrs = $6, zone_id = $7, group_id = $8, bid = $9  WHERE id = $10',
                               tag['name'], tag['mac'], tag['uuid'], tag['major'], tag['minor'],
                               json.dumps(tag['attrs']), tag['zone_id'], tag['group_id'], tag['bid'], t_id)
        raise web.HTTPNoContent

    async def delete(self):
        t_id = int(self.request.match_info['id'])
        async with self.request.app['db_pool'].acquire() as conn:
            await conn.execute('DELETE from tags where id = $1', t_id)
        raise web.HTTPNoContent
