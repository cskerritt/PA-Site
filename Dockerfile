# Purinton Analytics (pa-expert.com) - static site for Railway.
# Stage 1: regenerate every page from build.py (single source of truth).
FROM python:3.12-slim AS build
WORKDIR /app
COPY build.py content_practice.py content_insights.py ./
COPY favicon.svg ./
COPY assets ./assets
RUN python build.py \
    && rm -f build.py content_practice.py content_insights.py

# Stage 2: serve the generated static site with Caddy.
FROM caddy:2-alpine
COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=build /app /srv
