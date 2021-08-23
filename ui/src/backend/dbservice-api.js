import mozhiapi from "@/backend/mozhiapi"

class DBServiceAPI {

    constructor() {
    }

    create_db(connection_info, dbname){
        console.log(connection_info, dbname)
        let headers =   {
            timeout: 50000
        }
        // http://0.0.0.0:8088/mozhi/db/create?dbname=test123
        mozhiapi
            .post(process.env.VUE_APP_API_DB_CREATE + "?dbname=" + dbname, connection_info , headers)
            .then((res) => {
                console.log(res)
                return parseInt(res.data["count"])
            })
            .catch((err) => console.log(err))
            .finally(() => {
            })
    }

    get_db_list(connection_info) {
        let headers =   {
            timeout: 50000
        }
        return mozhiapi
            .post(process.env.VUE_APP_API_DB_DB_LIST, connection_info , headers)
            .then((res) => {
                return Promise.resolve(res.data["dblist"])
            })
            .catch((err) => {return Promise.reject(err)})
            .finally(() => {
            })
    }

    get_table_list(connection_info) {
        let headers =   {
            timeout: 50000
        }
        return mozhiapi
            .post(process.env.VUE_APP_API_DB_TABLE_LIST, connection_info , headers)
            .then((res) => {
                return Promise.resolve(res.data["tablelist"])
            })
            .catch((err) =>  {return Promise.reject(err)})
            .finally(() => {
            })
    }

    upload_text_files(formData) {
        console.info("upload_text_files formData", formData)
        let headers = {
            timeout: 50000,
            headers: {
                'Content-Type': 'multipart/form-data'
            },
            'Content-Type': 'multipart/form-data'
        }
        return mozhiapi
            .post(process.env.VUE_APP_API_DB_UPLOAD_TEXT_FILES, formData, headers)
            .then((res) => {
                // console.log(res)
                return Promise.resolve(res.data["uploadedpath"])
            })
            .catch(err => {
                if (err.message && err.message.includes('413')) {
                    console.log('The file you tried to upload is too large.')
                }
                return Promise.reject(err)
            })
    }

    get_tags(connection_info, tag_table_name) {
        let headers =   {
            timeout: 50000
        }
        return mozhiapi
            .post(process.env.VUE_APP_API_DB_GET_TAGS + "?tag_table_name="  + tag_table_name, connection_info, headers)
            .then((res) => {
                console.log(res)
                return Promise.resolve(res.data["tags"])
            })
            .catch((err) => {alert(err)
                return Promise.reject(err)})
            .finally(() => {
            })
    }

    save_tags(connection_info,
              id,
              tokens,
              labels,
              features_col_name,
              labels_col_name,
              text_table_name) {

        var data = {
            id: id,
            tokens: tokens,
            labels: labels,
            features_col_name: features_col_name,
            labels_col_name: labels_col_name,
            text_table_name: text_table_name,
            connection_info: connection_info,
        }

        return mozhiapi
            .post(process.env.VUE_APP_API_DB_TEXT_ANNOTATIONS,
                data,
                {timeout: 50000}) //TODO why "text" is needed ?
            .then((res) => {
                console.log("insert successfull", res)
            })
            .catch((err) => alert(err));
    }

    get_row(connection_info, row_id, texxt_table_name) {
        // http://0.0.0.0:8088/mozhi/db/text/get/row?table_name=conll20031_test&row_id=2
        let headers =   {
            timeout: 50000
        }

        return mozhiapi
            .post(process.env.VUE_APP_API_DB_GET_ROW + "?table_name="  + texxt_table_name + "&row_id=" + row_id,
                connection_info, headers)
            .then((res) => {
                console.log(res)
                return Promise.resolve(res)
            })
            .catch((err) => {alert(err)
                return Promise.reject(err)})
    }

    get_total_rows(connection_info, text_table_name) {
        //http://localhost:8088/mozhi/db/text/get/counts?text_table_name=conll2003_train

        console.log(connection_info, text_table_name)
        let headers =   {
            timeout: 50000
        }
        return mozhiapi
            .post(process.env.VUE_APP_API_DB_TEXT_COUNT + "?text_table_name=" + text_table_name, connection_info , headers)
            .then((res) => {
                console.log(res)
                return Promise.resolve(parseInt(res.data["count"]))
            })
            .catch((err) => {console.log(err)
                return Promise.reject(err)})
            .finally(() => {
            })
    }

    insert_annotated_data() {

    }

    insert_bbox_josn() {

    }

    get_fabric_json() {

    }
}

export default new DBServiceAPI();