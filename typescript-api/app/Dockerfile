FROM node:18

WORKDIR /usr/src/app
COPY . /usr/src/app/
RUN npm i -g pnpm
RUN pnpm install
RUN pnpm run init-project

EXPOSE 3000

CMD ["pnpm", "run", "start"]


