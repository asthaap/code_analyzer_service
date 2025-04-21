# Use Node.js image to build the frontend
FROM node:18 as build

WORKDIR /app

COPY . .

RUN npm install
RUN npm run build

# Use nginx to serve the built files
FROM nginx:stable-alpine as production

# Copy the build folder into nginx public dir
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom nginx config (optional)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
