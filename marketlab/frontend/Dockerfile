# Двухстадийный образ. На первом этапе собираем фронт через node, на втором - кладём в лёгкий nginx.
# Так в итоговый образ не попадает ни node_modules, ни сам node — только готовая статика.

FROM node:20-alpine AS builder
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install --no-audit --no-fund

COPY . .
RUN npm run build

FROM nginx:1.27-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
