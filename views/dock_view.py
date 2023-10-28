import json
from nss_handler import status
from repository import db_get_single, db_get_all, db_delete, db_update, db_create


class DocksView():

    def create(self, handler, dock_data):
        sql = """
        INSERT INTO DOCK (location, capacity)
        VALUES (?, ?)
        """
        db_new_id = db_create(
            sql, (dock_data['location'], dock_data['capacity']))

        if db_new_id:
            return handler.response(json.dumps({"id": db_new_id, "location": dock_data['location'], "capacity": dock_data['capacity']}), status.HTTP_201_SUCCESS_CREATED.value)
        else:
            return handler.response("Failed to create dock", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def get(self, handler, pk):
        url = handler.parse_url(handler.path)

        if pk != 0:
            dock = self.get_single_dock(pk, url.get("_embed"))
            return handler.response(json.dumps(dock), status.HTTP_200_SUCCESS.value)
        else:
            docks = self.get_all_docks(url.get("_embed"))
            return handler.response(json.dumps(docks), status.HTTP_200_SUCCESS.value)
        
    def get_single_dock(self, pk, embed_option):
        sql = "SELECT d.id, d.location, d.capacity FROM Dock d WHERE d.id = ?"
        query_results = db_get_single(sql, pk)
        dock = dict(query_results)

        if embed_option == 'hauler':
            self.get_embedded_hauler_info(dock)

        return dock
        
    def get_all_docks(self, embed_option):
        sql = "SELECT d.id, d.location, d.capacity FROM Dock d"
        query_results = db_get_all(sql)
        docks = [dict(row) for row in query_results]

        if embed_option == 'hauler':
            for dock in docks:
                self.get_embedded_hauler_info(dock)

        return docks    
    def get_embedded_hauler_info(self, dock):
        dock_id = dock.get('id')  # Get the dock's ID

        # Query the database for haulers matching the dock's ID
        hauler_sql = "SELECT h.id, h.name, h.dock_id FROM Hauler h WHERE h.dock_id = ?"
        query_results = db_get_all(hauler_sql, dock_id)

        # Create a list of hauler dictionaries
        haulers = [dict(row) for row in query_results]

        # Add the list of haulers to the dock dictionary under the key 'haulers'
        dock['haulers'] = haulers

    def delete(self, handler, pk):
        number_of_rows_deleted = db_delete("DELETE FROM Dock WHERE id = ?", pk)

        if number_of_rows_deleted > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def update(self, handler, dock_data, pk):
        sql = """
        UPDATE Dock
        SET
            location = ?,
            capacity = ?
        WHERE id = ?
        """
        number_of_rows_updated = db_update(
            sql,
            (dock_data['location'], dock_data['capacity'], pk)
        )

        if number_of_rows_updated > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
