#include <sqlite3.h>
#include <stdio.h>
#include <string.h>

int store_secret(const char *key, const char *value) {
    sqlite3 *db;
    char *err_msg = 0;
    int rc = sqlite3_open("vault.db", &db);
    
    if (rc != SQLITE_OK) return -1;

    char sql[512];
    snprintf(sql, sizeof(sql), "INSERT OR REPLACE INTO secrets (key, value) VALUES ('%s', '%s');", key, value);
    
    rc = sqlite3_exec(db, sql, 0, 0, &err_msg);
    sqlite3_close(db);
    return (rc == SQLITE_OK) ? 0 : -1;
}

char* get_secret(const char *key) {
    sqlite3 *db;
    sqlite3_stmt *res;
    char *value = NULL;
    
    if (sqlite3_open("vault.db", &db) != SQLITE_OK) return NULL;

    const char *sql = "SELECT value FROM secrets WHERE key = ?;";
    if (sqlite3_prepare_v2(db, sql, -1, &res, 0) == SQLITE_OK) {
        sqlite3_bind_text(res, 1, key, -1, SQLITE_STATIC);
        if (sqlite3_step(res) == SQLITE_ROW) {
            value = strdup((const char*)sqlite3_column_text(res, 0));
        }
    }
    sqlite3_finalize(res);
    sqlite3_close(db);
    return value;
}
