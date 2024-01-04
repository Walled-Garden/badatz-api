#FROM node:18
# todo: consider using oven/bun:1, see https://bun.sh/guides/ecosystem/docker
FROM node:18-alpine

WORKDIR /usr/src/app
COPY . /usr/src/app/
RUN npm i -g pnpm
RUN pnpm install
RUN pnpm run init-project
RUN pnpm run build-tsc

EXPOSE 5000

CMD ["pnpm", "run", "preview"]



## Stage 1: Build the application
#FROM node:18-alpine AS builder
#
#WORKDIR /usr/src/app
#COPY package.json pnpm-lock.yaml tsconfig.json /usr/src/app/
#RUN npm i -g pnpm
#RUN pnpm install
#COPY . /usr/src/app/
#RUN pnpm run init-project
#RUN pnpm run build-tsc
#
## Stage 2: Copy only the built application (dist directory) into a smaller image
#FROM node:18-alpine
#
#WORKDIR /usr/src/app
#COPY --from=builder /usr/src/app/dist /usr/src/app/dist
#COPY package.json /usr/src/app/
#COPY prisma /usr/src/app/prisma
#RUN npm i -g pnpm --production
#RUN pnpm run init-project
#EXPOSE 5000
#CMD ["pnpm", "run", "preview"]

