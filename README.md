# bank_system_api | WIP

If you need help, run:
```bash
make help
```

create a file `.env` on project for secret key
```bash
cd project/
```
```bash
echo "SECRET_KEY = {YOUR KEY HERE}" > .env
echo "ALGORITHM = HS256" >> .env
echo "ACCESS_TOKEN_EXP_MIN = 30" >> .env
```

create secret key on https://randomkeygen.com/

to config the enviroment, run all commands to activate the virtual enviroment
```bash
python3 -m venv venv --copies
```
```bash
make atvvenv
```
then follow the steps on make config
```bash
make config
```