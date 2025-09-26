DEFAULT		=	\033[0m
RED			=	\033[1;31m
CYAN		=	\033[1;36m
PINK		=	\033[1;35m
GREEN		=	\033[1;32m
YELLOW		=	\033[1;33m
REWHITE		=	\033[1;7;97m
RECYAN		=	\033[1;7;36m
REPINK		=	\033[1;7;35m
RERED		=	\033[1;7;31m
REGREEN		=	\033[1;7;32m
REYELLOW	=	\033[1;7;33m

help:
	@echo "${YELLOW}make depends${DEFAULT}:"
	@echo "${YELLOW}make api${DEFAULT}:"
	@echo "${YELLOW}make atvvenv${DEFAULT}:"
	@echo "${YELLOW}make init_db${DEFAULT}"
	@echo "${YELLOW}make init_db_migration${DEFAULT}:"
	@echo "${YELLOW}make upgrade_db${DEFAULT}:"
	@echo "${YELLOW}make config${DEFAULT}:"
# 	@echo "${YELLOW}${DEFAULT}:"
# 	@echo "${YELLOW}${DEFAULT}:"
# 	@echo "${YELLOW}${DEFAULT}:"

depends:
	@echo "${PINK}Installing all requirements...${DEFAULT}"
	@pip install -r requirements.txt
	@echo "${GREEN}Requirements installed successfully!${DEFAULT}"

api:
	@echo "${GREEN}Starting API...${DEFAULT}"
	@echo "${YELLOW}To stop the API from running, run CTRL + C${DEFAULT}"
	@uvicorn main:app --reload

atvvenv:
	@source venv/bin/activate

init_db:
	@alembic init alembic


init_db_migration:
	@alembic revision --autogenerate -m "init migration"

upgrade_db:
	@alembic upgrade head


config:
	@clear
	@sleep .5
	@echo "${YELLOW}Run ${PINK}make init_db${DEFAULT}"
	@sleep .5
	@echo ""
	@echo "${YELLOW}Then change ${GREEN}sqlalchemy.url${YELLOW} to ${CYAN}sqlite:///database.db${YELLOW} on ${PINK}alembic.ini${DEFAULT}"
	@sleep .5
	@echo ""
	@echo "${YELLOW}Then pass the following code to ${GREEN}env.py${YELLOW} at ${PINK}alembic/${DEFAULT}"
	@echo "${CYAN}-------------------------------------------------${DEFAULT}"
	@echo "${CYAN}import sys"
	@echo "import os"
	@echo ""
	@echo ""
	@echo "sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))"
	@echo ""
	@echo ""
	@echo "from models import Base{DEFAULT}"
	@echo "${CYAN}-------------------------------------------------${DEFAULT}"
	@sleep .5
	@echo ""
	@echo "${YELLOW}and change ${GREEN}target_metadata${YELLOW} value to ${CYAN}Base.metadata${DEFAULT}"
	@sleep .5
	@echo ""
	@echo "${YELLOW}Then run ${PINK}make init_db_migration${DEFAULT}"
	@sleep .5
	@echo ""
	@echo "${YELLOW}Finally run ${PINK}make upgrade_db${DEFAULT}"