class DBDetails {
    constructor(host, port, user, password, db_name, text_table_name, tag_table_name,
                text_col_name, features_col_name, labels_col_name, start_id) {
    self.host = host
    self.port = port
    self.user = user
    self.password = password
    self.db_name = db_name
    self.text_table_name = text_table_name
    self.tag_table_name = tag_table_name
    self.text_col_name = text_col_name
    self.features_col_name = features_col_name
    self.labels_col_name = labels_col_name
    self.start_id = start_id
    }
}