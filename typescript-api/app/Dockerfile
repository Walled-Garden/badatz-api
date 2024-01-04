FROM node:18
# todo: consider using oven/bun:1, see https://bun.sh/guides/ecosystem/docker

WORKDIR /usr/src/app
COPY . /usr/src/app/
RUN npm i -g pnpm
RUN pnpm install
RUN pnpm run init-project
RUN pnpm run build-tsc

EXPOSE 5000

CMD ["pnpm", "run", "preview"]


