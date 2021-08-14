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
            .catch((error) => {
                return Promise.reject(error)
            })
    }

    get_table() {

    }

    get_row() {

    }

    get_total_rows(connection_info, text_table_name) {
        //http://localhost:8088/mozhi/db/text/get/counts?text_table_name=conll2003_train

        console.log(connection_info, text_table_name)
        let headers =   {
            timeout: 50000
        }
        mozhiapi
            .post(process.env.VUE_APP_API_DB_TEXT_COUNT + "?text_table_name=" + text_table_name, connection_info , headers)
            .then((res) => {
                console.log(res)
                return parseInt(res.data["count"])
            })
            .catch((err) => console.log(err))
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