import mozhiapi from "@/backend/mozhiapi"


class MinIOServiceAPI {

    get_file_prefixes(connection_info, bucket, prefix) {
        console.log(connection_info, bucket, prefix)
        //http://0.0.0.0:8088/mozhi/storage/minio/list?bucket=mozhi&prefix=data%2Freceipts
        let headers =   {
            timeout: 50000
        }

        return mozhiapi
            .post(process.env.VUE_APP_API_MINIO_LIST + `?bucket=${bucket}&prefix=${prefix}`, connection_info, headers)
            .then((res) => {
                console.log(res)
                return Promise.resolve(res.data)
            })
            .catch((err) => {alert(err)
                return Promise.reject(err)
            })
    }

    create_annotation_table(db_connection_info, experiment_name) {
        let headers =   {
            timeout: 50000
        }
        // Create the image table to hold image annotations
        mozhiapi
            .post(process.env.VUE_APP_API_DB_IMAGE_CREATE,
                {"db_connection_info": db_connection_info, "experiment_name": experiment_name}, headers)
            .then((res) => {
                console.log(res)
            })
            .catch((err) => alert(err))
            .finally(() => {
                console.log("finally: image annotation table created successfully!")
            })
    }

    get_bbox_json(db_connection_info, experimentName, fileCurrentPrefix) {
        // let headers =   {
        //     timeout: 50000
        // }

        return mozhiapi
            .post(process.env.VUE_APP_API_DB_IMAGE_BBOX_GET,
                {'db_connection_info': db_connection_info,
                    'experiment_name': experimentName,
                    'prefix': fileCurrentPrefix})
            .then((res) => {
                return Promise.resolve(res)
            })
            .catch((err) => {alert(err)
                return Promise.reject(err)
            })
    }

    insert_bbox_json(db_connection_info,
                     experiment_name,
                     prefix,
                     bbox_json,
                     ocr_text) {
        // let headers =   {
        //     timeout: 50000
        // }

        return mozhiapi
            .post(process.env.VUE_APP_API_DB_IMAGE_BBOX_INSERT,
                {'db_connection_info': db_connection_info,
                    'experiment_name': experiment_name,
                    'prefix': prefix,
                    'bbox_json': bbox_json,
                    'ocr_text': ocr_text})
            .then((res) => {
                return Promise.resolve(res)
            })
            .catch((err) => {alert(err)
                return Promise.reject(err)
            })
    }

    get_text(bucket, fileCurrentPrefix, connection_info) {
        const body = {'bucket': bucket,
            'prefix': fileCurrentPrefix,
            'connection_info': connection_info}
        mozhiapi.defaults.timeout = 30000;
        return mozhiapi
            .post(process.env.VUE_APP_API_MINIO_GET_TEXT, body)
            .then(res => {
                return Promise.resolve(res["data"]['text'])
                // console.info(res);
            })
            .catch((err) => {alert(err)
                return Promise.reject(err)
            })
    }

    get_text_info(bucket, fileCurrentPrefix, connection_info) {
        const body = {'bucket': bucket,
            'prefix': fileCurrentPrefix,
            'connection_info': connection_info}
        mozhiapi.defaults.timeout = 30000;
        return mozhiapi
            .post(process.env.VUE_APP_API_MINIO_GET_TEXTINFO, body)
            .then(res => {
                return Promise.resolve(res["data"]['text'])
                // console.info(res);
            })
            .catch((err) => {alert(err)
                return Promise.reject(err)
            })
    }

    set_policy(bucket, filePrefix, connection_info) {
        const body = {'bucket': bucket,
            'prefix': filePrefix,
            'connection_info': connection_info}
        return mozhiapi
            .post(process.env.VUE_APP_API_MINIO_SET_POLICY, body)
            .then(res => {
                return Promise.resolve(res)
                // console.info(res);
            })
            .catch((err) => {alert(err)
                return Promise.reject(err)
            })

    }
}

export default new MinIOServiceAPI()