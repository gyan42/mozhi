export default class UserLogInfo {
  constructor(username, password, grant_type, scope, client_id, client_secret) {
        this.grant_type = grant_type
        this.username = username
        this.password = password
        this.scope = scope
        this.client_id = client_id
        this.client_secret = client_secret
  }
}