import json
from nss_handler import status
from repository import db_get_single, db_get_all, db_delete, db_update, db_create


class HaulerView():

    def create(self, handler, hauler_data):
        sql = """
        INSERT INTO HAULER (name, dock_id)
        VALUES (?, ?)
        """
        db_new_id = db_create(
            sql, (hauler_data['name'], hauler_data['dock_id']))

        if db_new_id:
            return handler.response(json.dumps({"id": db_new_id, "name": hauler_data['name'], "dock_id": hauler_data['dock_id']}), status.HTTP_201_SUCCESS_CREATED.value)
        else:
            return handler.response("Failed to create hauler", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def get(self, handler, pk, url):
        if pk != 0:
            if "_expand" in url:
                sql = """
                    SELECT
                        h.id,
                        h.name,
                        h.dock_id,
                        d.id dockId,
                        d.location dockLocation,
                        d.capacity
                    FROM Hauler h
                    JOIN Dock d
                    ON h.dock_id = d.id
                    WHERE h.id = ?
                """
                query_results = db_get_single(sql, pk)
                query_result = dict(query_results)
                dock = {
                    "id": query_result['dockId'],
                    "location": query_result['dockLocation'],
                    "capacity": query_result['capacity']
                }
                hauler = {
                    "id": query_result['id'],
                    "name": query_result['name'],
                    "dock_id": query_result['dock_id'],
                    "dock": dock
                }
                serialized_hauler = json.dumps(dict(hauler))
                return handler.response(serialized_hauler, status.HTTP_200_SUCCESS.value)

            else:
                sql = """
                    SELECT
                        h.id,
                        h.name,
                        h.dock_id
                    FROM Hauler h
                    WHERE h.id = ?
                """
                query_results = db_get_single(sql, pk)
                query_result = dict(query_results)
                hauler = {
                    "id": query_result['id'],
                    "name": query_result['name'],
                    "dock_id": query_result['dock_id'],
                }
                serialized_hauler = json.dumps(dict(hauler))
                return handler.response(serialized_hauler, status.HTTP_200_SUCCESS.value)

        else:
            sql = "SELECT h.id, h.name, h.dock_id FROM Hauler h"
            query_results = db_get_all(sql)
            haulers = [dict(row) for row in query_results]
            serialized_haulers = json.dumps(haulers)

            return handler.response(serialized_haulers, status.HTTP_200_SUCCESS.value)

    def delete(self, handler, pk):
        number_of_rows_deleted = db_delete(
            "DELETE FROM Hauler WHERE id = ?", pk)

        if number_of_rows_deleted > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def update(self, handler, hauler_data, pk):
        sql = """
        UPDATE Hauler
        SET
            name = ?,
            dock_id = ?
        WHERE id = ?
        """
        number_of_rows_updated = db_update(
            sql,
            (hauler_data['name'], hauler_data['dock_id'], pk)
        )

        if number_of_rows_updated > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
