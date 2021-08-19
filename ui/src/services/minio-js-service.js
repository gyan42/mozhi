
// Example anonymous read-only bucket policy.
// policy = {
//     "Version": "2012-10-17",
//     "Statement": [
//         {
//             "Effect": "Allow",
//             "Principal": {"AWS": "*"},
//             "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
//             "Resource": "arn:aws:s3:::my-bucket",
//         },
//         {
//             "Effect": "Allow",
//             "Principal": {"AWS": "*"},
//             "Action": "s3:GetObject",
//             "Resource": "arn:aws:s3:::my-bucket/*",
//         },
//     ],
// }
//
// // Example anonymous read-write bucket policy.
// policy = {
//     "Version": "2012-10-17",
//     "Statement": [
//         {
//             "Effect": "Allow",
//             "Principal": {"AWS": "*"},
//             "Action": [
//                 "s3:GetBucketLocation",
//                 "s3:ListBucket",
//                 "s3:ListBucketMultipartUploads",
//             ],
//             "Resource": "arn:aws:s3:::my-bucket",
//         },
//         {
//             "Effect": "Allow",
//             "Principal": {"AWS": "*"},
//             "Action": [
//                 "s3:GetObject",
//                 "s3:PutObject",
//                 "s3:DeleteObject",
//                 "s3:ListMultipartUploadParts",
//                 "s3:AbortMultipartUpload",
//             ],
//             "Resource": "arn:aws:s3:::my-bucket/images/*",
//         },
//     ],
// }

import Minio from "minio"

// var Minio = require('minio')

class MinIOJSService {
    constructor(host, port, accessKey, secretKey) {
        this.minio = new Minio({
            endPoint: host,
            port: port,
            useSSL: false,
            accessKey: accessKey,
            secretKey: secretKey
        });
    }

    set_download_policy(bucket, prefix) {
        let policy = `{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
                    "Resource": "arn:aws:s3:::my-bucket",
                },
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": "s3:GetObject",
                    "Resource": "arn:aws:s3:::${bucket}/${prefix}",
                },
            ],
        }`

        this.minio.setBucketPolicy(bucket, JSON.stringify(policy), function(err) {
            if (err) throw err
            console.log('Bucket policy set')
        })
    }
}

export default MinIOJSService