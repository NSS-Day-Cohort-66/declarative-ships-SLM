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

    def get(self, handler, pk):
        # Parse the URL
        url = handler.parse_url(handler.path)

        if pk != 0:
            hauler = self.get_single_hauler(pk, url.get("_expand"))
            return handler.response(json.dumps(hauler), status.HTTP_200_SUCCESS.value)
        else:
            haulers = self.get_all_haulers(url.get("_expand"))
            return handler.response(json.dumps(haulers), status.HTTP_200_SUCCESS.value)

    def get_single_hauler(self, pk, expand_option):
        sql = "SELECT h.id, h.name, h.dock_id FROM Hauler h WHERE h.id = ?"
        query_results = db_get_single(sql, pk)
        hauler = dict(query_results)

        if expand_option == 'dock':
            self.get_expanded_dock_info(hauler)

        return hauler

    def get_all_haulers(self, expand_option):
        sql = "SELECT h.id, h.name, h.dock_id FROM Hauler h"
        query_results = db_get_all(sql)
        haulers = [dict(row) for row in query_results]

        if expand_option == 'dock':
            for hauler in haulers:
                self.get_expanded_dock_info(hauler)

        return haulers

    def get_expanded_dock_info(self, hauler):
        dock_id = hauler.get('dock_id')
        if dock_id != 0:
            dock_sql = "SELECT d.id, d.location, d.capacity FROM Dock d WHERE d.id = ?"
            dock_info = db_get_single(dock_sql, dock_id)
            hauler['dock'] = dict(dock_info)

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
