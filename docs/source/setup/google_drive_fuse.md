# Google Drive Fuse

Commands and steps to fuse Google drive to Colab notebook.

```shell
pip install --upgrade pip
pip install -U -q pydrive
apt-get install -y -qq software-properties-common python-software-properties module-init-tools
add-apt-repository -y ppa:alessandro-strada/ppa 2>&1 > /dev/null
apt-get update -qq 2>&1 > /dev/null

apt-get -y install -qq google-drive-ocamlfuse fuse
```

```python
from google.colab import auth
auth.authenticate_user()
# Generate creds for the Drive FUSE library.
from oauth2client.client import GoogleCredentials
creds = GoogleCredentials.get_application_default()
print(creds.client_id, creds.client_secret)
import getpass
vcode = getpass.getpass()
```

```
google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret} < /dev/null 2>&1 | grep URL
echo {vcode} | google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret}
```

```
mkdir -p drive
google-drive-ocamlfuse drive
```