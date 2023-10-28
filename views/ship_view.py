import sqlite3
import json
from nss_handler import status
from repository import db_get_single, db_get_all, db_delete, db_update, db_create


class ShippingShipsView():

    def create(self, handler, ship_data):
        sql = """
        INSERT INTO ship (name, hauler_id)
        VALUES (?, ?)
        """
        db_new_id = db_create(
            sql, (ship_data['name'], ship_data['hauler_id']))

        if db_new_id:
            return handler.response(json.dumps({"id": db_new_id, "name": ship_data['name'], "hauler_id": ship_data['hauler_id']}), status.HTTP_201_SUCCESS_CREATED.value)
        else:
            return handler.response("Failed to create ship", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def get(self, handler, pk):
        url = handler.parse_url(handler.path)

        if pk != 0:
            ship = self.get_single_ship(pk, url.get("_expand"))
            return handler.response(json.dumps(ship), status.HTTP_200_SUCCESS.value)
        else:
            ships = self.get_all_ships(url.get("_expand"))
            return handler.response(json.dumps(ships), status.HTTP_200_SUCCESS.value)
        
    def get_single_ship(self, pk, expand_option):
        sql = "SELECT s.id, s.name, s.hauler_id FROM Ship s WHERE s.id = ?"
        query_results = db_get_single(sql, pk)
        ship = dict(query_results)

        if expand_option == 'hauler':
            self.get_expanded_hauler_info(ship)

        return ship
        
    def get_all_ships(self, expand_option):
        sql = "SELECT s.id, s.name, s.hauler_id FROM Ship s"
        query_results = db_get_all(sql)
        ships = [dict(row) for row in query_results]

        if expand_option == 'hauler':
            for ship in ships:
                self.get_expanded_hauler_info(ship)

        return ships    
    def get_expanded_hauler_info(self, ship):
        hauler_id = ship.get('hauler_id')
        if hauler_id != 0:
            hauler_sql = "SELECT h.id, h.name FROM Hauler h WHERE h.id = ?"
            hauler_info = db_get_single(hauler_sql, hauler_id)
            ship['hauler'] = dict(hauler_info)

    def delete(self, handler, pk):
        number_of_rows_deleted = db_delete("DELETE FROM Ship WHERE id = ?", pk)

        if number_of_rows_deleted > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def update(self, handler, ship_data, pk):
        sql = """
        UPDATE Ship
        SET
            name = ?,
            hauler_id = ?
        WHERE id = ?
        """
        number_of_rows_updated = db_update(
            sql,
            (ship_data['name'], ship_data['hauler_id'], pk)
        )

        if number_of_rows_updated > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
