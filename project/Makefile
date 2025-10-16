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
	@clear
	@echo "${YELLOW}make init_venv${DEFAULT} or ${YELLOW}python3 -m venv venv --copies${DEFAULT}: create virtual enviroment"
	@echo "${YELLOW}make atvvenv${DEFAULT}:activate the virtual enviroment"
	@echo "${YELLOW}make depends${DEFAULT}: install all dependencies"
	@echo "${YELLOW}make config${DEFAULT}: Step-to-step on how to config your machine to run this project"
	@echo "${YELLOW}make init_db${DEFAULT}: start the alambic (1/3)"
	@echo "${YELLOW}make init_db_migration${DEFAULT}: start the database (2/3)"
	@echo "${YELLOW}make upgrade_db${DEFAULT}: finish creating the database (3/3)"
	@echo "${YELLOW}make api${DEFAULT}: start the API"
	@echo "${YELLOW}deactivate${DEFAULT}:deactivate the virtual enviroment"
	@echo "${YELLOW}make remove_venv${DEFAULT}:delete the virtual enviroment"


depends:
	@echo "${PINK}Installing all requirements...${DEFAULT}"
	@pip install -r requirements.txt
	@echo "${GREEN}Requirements installed successfully!${DEFAULT}"


api:
	@echo "${GREEN}Starting API...${DEFAULT}"
	@echo "${YELLOW}To stop the API from running, run CTRL + C${DEFAULT}"
	@uvicorn main:app --reload


init_venv:
	@python3 -m venv venv --copies


atvvenv:
	@echo "${YELLOW}Run: ${PINK}source venv/bin/activate${DEFAULT}"


remove_venv:
	@rm -rfd venv


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
	@echo "from models import Base"
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

destroy_echo:
	@clear
	@echo "${RED}WARNING, ALL PROGRAM WILL BE DESTROYED, RUN ${CYAN}CTRL + C${RED} TO ABORT THE DESTRUCTION!${DEFAULT}"
	@echo "${YELLOW}Starting in 5...${DEFAULT}"
	@sleep 1
	@clear
	@echo "${RED}WARNING, ALL PROGRAM WILL BE DESTROYED, RUN ${CYAN}CTRL + C${RED} TO ABORT THE DESTRUCTION!${DEFAULT}"
	@echo "${YELLOW}Starting in 4...${DEFAULT}"
	@sleep 1
	@clear
	@echo "${RED}WARNING, ALL PROGRAM WILL BE DESTROYED, RUN ${CYAN}CTRL + C${RED} TO ABORT THE DESTRUCTION!${DEFAULT}"
	@echo "${YELLOW}Starting in 3...${DEFAULT}"
	@sleep 1
	@clear
	@echo "${RED}WARNING, ALL PROGRAM WILL BE DESTROYED, RUN ${CYAN}CTRL + C${RED} TO ABORT THE DESTRUCTION!${DEFAULT}"
	@echo "${YELLOW}Starting in 2...${DEFAULT}"
	@sleep 1
	@clear
	@echo "${RED}WARNING, ALL PROGRAM WILL BE DESTROYED, RUN ${CYAN}CTRL + C${RED} TO ABORT THE DESTRUCTION!${DEFAULT}"
	@echo "${YELLOW}Starting in 1...${DEFAULT}"
	@sleep 1
	@clear
	@echo "${RED}WARNING, ALL PROGRAM WILL BE DESTROYED, RUN ${CYAN}CTRL + C${RED} TO ABORT THE DESTRUCTION!${DEFAULT}"
	@echo "${YELLOW}Starting in 0...${DEFAULT}"
	@sleep 1
	@clear


clean:
	@clear
	@make destroy_echo
	@clear
	@echo "${YELLOW}Destruction started!${DEFAULT}"
	@sleep 2
	@clear
	@echo "${PINK}Destroying venv/...${DEFAULT}"
	@rm -rfd venv
	@sleep 2
	@clear
	@echo "${PINK}Destroying alembic/...${DEFAULT}"
	@rm -rfd alembic
	@sleep 2
	@clear
	@echo "${PINK}Destroying all pycache...${DEFAULT}"
	@find . -name "__pycache__" -type d -exec rm -rf {} +
	@sleep 2
	@clear
	@echo "${PINK}Destroying database.db and alembic.ini${DEFAULT}"
	@rm database.db alembic.ini
	@sleep 3
	@clear
	@echo "$(GREEN)Program cleaned successfully!$(DEFAULT)"